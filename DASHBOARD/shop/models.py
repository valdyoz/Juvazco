import random
from decimal import Decimal
from django.db import models
from alamatseller import SELLER_DATA, seller_by_name


class Product(models.Model):
    nama_produk = models.CharField(max_length=150)
    kategori = models.CharField(max_length=100, blank=True)
    deskripsi = models.TextField(blank=True)
    harga = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stok = models.PositiveIntegerField(default=0)
    gambar = models.ImageField(upload_to='product_images/', blank=True, null=True)
    seller_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.seller_name:
            self.seller_name = random.choice(SELLER_DATA)['nama']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_produk

    @property
    def seller_photo(self):
        return seller_by_name(self.seller_name)['foto']

    @property
    def harga_int(self):
        return int(self.harga or Decimal('0'))


class CartItem(models.Model):
    session_key = models.CharField(max_length=120)
    username_customer = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.harga * self.jumlah

    def __str__(self):
        return f'{self.username_customer} - {self.product.nama_produk}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
    ]
    username_customer = models.CharField(max_length=100)
    nama_customer = models.CharField(max_length=120)
    daerah = models.CharField(max_length=150)
    alamat_lengkap = models.TextField()
    no_hp = models.CharField(max_length=30)
    metode_pembayaran = models.CharField(max_length=50, default='COD')
    catatan = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.nama_customer}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    nama_produk = models.CharField(max_length=150)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    jumlah = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.nama_produk} x {self.jumlah}'
