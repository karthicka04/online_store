from django.db import models
from accounts.models import CustomUser

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return self.name
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped')])
    def __str__(self):
        return f"Order: {self.product.name} by {self.customer.username}"
class Cart(models.Model):
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.customer.username}'s Cart"
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
         return f"{self.quantity} x {self.product.name} in {self.cart.customer.username}'s Cart"


