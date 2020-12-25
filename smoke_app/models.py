from django.db import models
import re

class UserManager(models.Manager):
    def create_user(self, data):
        pw_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = pw_hash,
        )
        return user

    def get_user(self, id):
        return User.objects.filter(id = id).first()

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# ======================================================================

class ProductManager(models.Manager):
    def create_product(self, data):
        product = Product.objects.create(
            name = data['name'],
            category = data['category'],
            description = data['description'],
            price = data['price'],
            stock = data['stock']
        )
        return product

    def get_product(self, id):
        return Product.objects.filter(id = id).first()

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

# ======================================================================

class OrderManager(models.Manager):
    def create_order(self, user_id):
        user = User.objects.get_user(user_id)
        cart_items = Cart.objects.filter(user)
        total_price = 0
        if cart_items:
            order = Order.objects.create()
            for item in cart_items:
                total_price += item.product.price * item.quantity
                order.cart_items.add(item)
            order.total_price = total_price
            order.save()
            return order

    def get_order(self, id):
        return Order.objects.filter(id = id).first()

class Order(models.Model):
    status = models.CharField(max_length=100, default='ordered')
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()

# ======================================================================

class CartManager(models.Manager):
    def create_cart_item(self, user_id, product_id, data):
        user = User.objects.get_user(user_id)
        product = Product.objects.get_product(product_id)
        cart_item = Cart.objects.create(
            user = user,
            product = product,
            quantity = data['quantity']
        )
        return cart_item

    def get_cart_item(self, id):
        return Cart.objects.filter(id = id).first()

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='cart_items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CartManager()
