import random
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from AdminUser import cek_login, ambil_semua_user
from alamatseller import DAERAH_INDONESIA
from .forms import ProductForm
from .models import Product, CartItem, Order, OrderItem
from django.http import JsonResponse
from .models import CartItem

def get_cart_count(request):
    # Pakai session manual, bukan Django auth
    if request.session.get('is_login') and request.session.get('role') == 'customer':
        session_key = request.session.session_key
        username = request.session.get('username')
        count = CartItem.objects.filter(
            session_key=session_key,
            username_customer=username
        ).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


def is_login(request):
    return request.session.get('is_login') is True


def is_admin(request):
    return request.session.get('role') == 'admin'


def is_customer(request):
    return request.session.get('role') == 'customer'


def ensure_session(request):
    if not request.session.session_key:
        request.session.create()

def home(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all().order_by('-id')
    if query:
        products = products.filter(nama_produk__icontains=query)
    return render(request, 'home.html', {
        'products': products,
        'query': query,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'customer/product_detail.html', {'product': product})


def login_view(request):
    if is_login(request):
        if is_admin(request):
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email', '')
        password = request.POST.get('password', '')
        akun = cek_login(username_or_email, password)
        if akun:
            request.session['is_login'] = True
            request.session['username'] = akun['username']
            request.session['email'] = akun['email']
            request.session['nama'] = akun['nama']
            request.session['role'] = akun['role']
            if akun['role'] == 'admin':
                return redirect('admin_dashboard')
            return redirect('home')
        messages.error(request, 'Username/email atau password salah.')
    return render(request, 'login.html')


def register_view(request):
    return render(request, 'register.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


def admin_dashboard(request):
    if not is_login(request) or not is_admin(request):
        return redirect('login')
    products = Product.objects.all().order_by('-id')
    orders = Order.objects.all().order_by('-tanggal')[:6]
    users = ambil_semua_user()
    total_pendapatan = sum([order.total for order in Order.objects.all()], Decimal('0'))
    return render(request, 'admin/dashboard_admin.html', {
        'products': products,
        'orders': orders,
        'users': users,
        'total_produk': Product.objects.count(),
        'total_pesanan': Order.objects.count(),
        'total_customer': len([user for user in users if user['role'] == 'customer']),
        'total_pendapatan': total_pendapatan,
    })


def admin_product_add(request):
    if not is_login(request) or not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan.')
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form, 'mode': 'Tambah'})


def admin_product_edit(request, product_id):
    if not is_login(request) or not is_admin(request):
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diedit.')
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form, 'mode': 'Edit', 'product': product})


def admin_product_delete(request, product_id):
    if not is_login(request) or not is_admin(request):
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Produk berhasil dihapus.')
    return redirect('admin_dashboard')


def admin_orders(request):
    if not is_login(request) or not is_admin(request):
        return redirect('login')
    orders = Order.objects.all().order_by('-tanggal')
    return render(request, 'admin/orders.html', {'orders': orders})


def add_to_cart(request, product_id):
    if not is_login(request) or not is_customer(request):
        messages.warning(request, 'Login sebagai customer dulu untuk menambahkan keranjang.')
        return redirect('login')
    ensure_session(request)
    product = get_object_or_404(Product, id=product_id)
    jumlah = int(request.POST.get('jumlah', 1))
    item, created = CartItem.objects.get_or_create(
        session_key=request.session.session_key,
        username_customer=request.session.get('username'),
        product=product,
        defaults={'jumlah': jumlah}
    )
    if not created:
        item.jumlah += jumlah
        item.save()
    messages.success(request, 'Produk masuk ke keranjang.')
    return redirect('cart')


def cart_view(request):
    if not is_login(request) or not is_customer(request):
        messages.warning(request, 'Login sebagai customer dulu untuk membuka keranjang.')
        return redirect('login')
    ensure_session(request)
    items = CartItem.objects.filter(
        session_key=request.session.session_key,
        username_customer=request.session.get('username')
    )
    total = sum([item.subtotal() for item in items], Decimal('0'))
    return render(request, 'customer/cart.html', {'items': items, 'total': total})


def remove_cart_item(request, item_id):
    if not is_login(request) or not is_customer(request):
        return redirect('login')
    CartItem.objects.filter(id=item_id, username_customer=request.session.get('username')).delete()
    return redirect('cart')


def make_captcha(request):
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    request.session['captcha_answer'] = a + b
    return f'{a} + {b}'


def captcha_ok(request):
    return request.POST.get('captcha', '').strip() == str(request.session.get('captcha_answer', ''))


def checkout_cart(request):
    if not is_login(request) or not is_customer(request):
        messages.warning(request, 'Login sebagai customer dulu untuk checkout.')
        return redirect('login')
    ensure_session(request)
    items = CartItem.objects.filter(
        session_key=request.session.session_key,
        username_customer=request.session.get('username')
    )
    if not items.exists():
        messages.warning(request, 'Keranjang masih kosong.')
        return redirect('home')
    total = sum([item.subtotal() for item in items], Decimal('0'))
    if request.method == 'POST':
        if not captcha_ok(request):
            messages.error(request, 'Captcha salah, coba lagi.')
            return render(request, 'customer/checkout.html', {'items': items, 'total': total, 'daerah': DAERAH_INDONESIA, 'captcha': make_captcha(request)})
        order = create_order_from_items(request, items, total)
        items.delete()
        return redirect('checkout_loading', order_id=order.id)
    return render(request, 'customer/checkout.html', {'items': items, 'total': total, 'daerah': DAERAH_INDONESIA, 'captcha': make_captcha(request)})


def checkout_direct(request, product_id):
    if not is_login(request) or not is_customer(request):
        messages.warning(request, 'Login sebagai customer dulu untuk checkout.')
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    jumlah = int(request.POST.get('jumlah', 1)) if request.method == 'POST' else 1
    item_temp = [{'product': product, 'jumlah': jumlah, 'subtotal': product.harga * jumlah}]
    total = product.harga * jumlah
    if request.method == 'POST' and request.POST.get('submit_checkout') == '1':
        if not captcha_ok(request):
            messages.error(request, 'Captcha salah, coba lagi.')
            return render(request, 'customer/checkout.html', {'items': item_temp, 'total': total, 'daerah': DAERAH_INDONESIA, 'captcha': make_captcha(request), 'direct_product': product, 'direct_jumlah': jumlah})
        order = create_order_from_items(request, item_temp, total)
        return redirect('checkout_loading', order_id=order.id)
    return render(request, 'customer/checkout.html', {'items': item_temp, 'total': total, 'daerah': DAERAH_INDONESIA, 'captcha': make_captcha(request), 'direct_product': product, 'direct_jumlah': jumlah})


def create_order_from_items(request, items, total):
    order = Order.objects.create(
        username_customer=request.session.get('username'),
        nama_customer=request.session.get('nama'),
        daerah=request.POST.get('daerah', ''),
        alamat_lengkap=request.POST.get('alamat_lengkap', ''),
        no_hp=request.POST.get('no_hp', ''),
        metode_pembayaran=request.POST.get('metode_pembayaran', 'COD'),
        catatan=request.POST.get('catatan', ''),
        total=total,
    )
    for item in items:
        product = item['product'] if isinstance(item, dict) else item.product
        jumlah = item['jumlah'] if isinstance(item, dict) else item.jumlah
        subtotal = item['subtotal'] if isinstance(item, dict) else item.subtotal()
        OrderItem.objects.create(
            order=order,
            product=product,
            nama_produk=product.nama_produk,
            harga=product.harga,
            jumlah=jumlah,
            subtotal=subtotal,
        )
        if product.stok >= jumlah:
            product.stok -= jumlah
            product.save()
    return order


def checkout_loading(request, order_id):
    if not is_login(request):
        return redirect('login')
    return render(request, 'customer/loading.html', {'order_id': order_id})


def order_success(request, order_id):
    if not is_login(request):
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'customer/order_success.html', {'order': order})


def customer_service(request):
    if not is_login(request) or not is_customer(request):
        return redirect('login')
    return render(request, 'customer/customer_service.html')

def developer_view(request):
    return render(request, 'developer.html')
