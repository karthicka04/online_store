from django.urls import path
from .views import admin_dashboard, vendor_dashboard,browse_products,add_product,manage_products, view_orders,add_to_cart, view_cart, checkout,check_products,buy_now, view_all_users,view_vendors

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('products/', browse_products, name='browse_products'),
    path('add-product/', add_product, name='add_product'),
    path('manage-products/', manage_products, name='manage_products'),
    path('view-orders/', view_orders, name='view_orders'), 
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('check-products/', check_products),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
    path('admin/all-users/', view_all_users, name='view_all_users'),
    path('admin/vendors/', view_vendors, name='view_vendors'),
]   
