from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Order , Cart ,CartProduct , CustomUser
from .forms import ProductForm

def is_admin(user):
     return user.is_superuser or user.role == 'admin'

def is_vendor(user):
    return user.role == 'vendor'

def is_customer(user):
    return user.role == 'customer'
def is_vendor_or_admin(user):
    return user.is_superuser or user.role == 'vendor'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    return render(request, 'store/admin_dashboard.html', {'products': products, 'orders': orders})

@login_required
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    products = Product.objects.filter(vendor=request.user)
    orders = Order.objects.filter(product__vendor=request.user)
    return render(request, 'store/vendor_dashboard.html', {'products': products, 'orders': orders})
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)  # If you have file fields, include request.FILES
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user  # Assuming the vendor is the logged-in user
            product.save()
            return redirect('vendor_dashboard')  # Redirect to the vendor dashboard or any other page
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})

@login_required
@user_passes_test(is_vendor_or_admin)
def manage_products(request):
    # Retrieve all products added by the logged-in vendor
    products = Product.objects.filter(vendor=request.user)

    # Handle product deletion
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_to_delete = Product.objects.get(id=product_id, vendor=request.user)
        product_to_delete.delete()
        return redirect('manage_products')

    return render(request, 'store/manage_products.html', {'products': products})
 

@login_required
@user_passes_test(is_vendor_or_admin)

def view_orders(request):
    # Get the vendor's products
    vendor_products = Product.objects.filter(vendor=request.user)
    
    # Get the orders associated with the vendor's products
    orders = Order.objects.filter(product__in=vendor_products).select_related('customer', 'product')
    
    # Pass the orders to the template
    return render(request, 'store/view_orders.html', {'orders': orders})


@login_required
@user_passes_test(is_customer)
def browse_products(request):
    products = Product.objects.all()
    return render(request, 'store/browse_products.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)

    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    cart_product.quantity += 1
    cart_product.save()

    return redirect('browse_products')
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = 1  # Set the quantity, or get it from the request

    # Create an order for the product
    order = Order.objects.create(product=product, customer=request.user, quantity=1, status='pending')

    return redirect('browse_products')

def view_cart(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = cart.cartproduct_set.all()  # Accessing related `CartProduct` objects
    return render(request, 'store/view_cart.html', {'cart_items': cart_items})

def checkout(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = cart.cartproduct_set.all()
    
    # Logic to handle checkout, payment, etc.
    cart_items.delete()  # Clear the cart after checkout
    return render(request, 'store/checkout.html')

def home(request):
    return render(request, 'store/home.html')
def check_products(request):
    products = Product.objects.all()
    for product in products:
        print(product.name, product.price)
    return HttpResponse("Check the console for product list.")
@login_required
@user_passes_test(is_admin)
def view_all_users(request):
    users = CustomUser.objects.all()
    return render(request, 'store/admin_all_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def view_vendors(request):
    vendors = CustomUser.objects.filter(role='vendor')
    return render(request, 'store/admin_vendors.html', {'vendors': vendors})