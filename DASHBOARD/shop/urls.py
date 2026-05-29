from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produk/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-dashboard/products/edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-dashboard/products/delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    path('admin-dashboard/orders/', views.admin_orders, name='admin_orders'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/cart/', views.checkout_cart, name='checkout_cart'),
    path('checkout/direct/<int:product_id>/', views.checkout_direct, name='checkout_direct'),
    path('checkout/loading/<int:order_id>/', views.checkout_loading, name='checkout_loading'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('developer/', views.developer_view, name='developer'),
]