from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def create_user(self, data):
        pw_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = pw_hash,
            is_admin = data['is_admin']
        )
        return user

    def get_user(self, id):
        user = User.objects.filter(id = id).first()
        return user

    def update_user(self, data):
        user = User.objects.filter(id = data['id']).first()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.password = data['password']
        user.is_admin = data['is_admin']
        user.save()

    def delete_user(self, id):
        user = User.objects.filter(id = id).first()
        user.delete()

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

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
        product = Product.objects.filter(id = id).first()
        return product

    def update_product(self, data):
        product = Product.objects.filter(id = data['id']).first()
        product.name = data['name']
        product.category = data['category']
        product.description = data['description']
        product.price = data['price']
        product.stock = data['stock']
        product.save()

    def delete_product(self, id):
        product = Product.objects.filter(id = id).first()
        product.delete()

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

class OrderManager(models.Manager):
    def create_order(self, data):
        order = Order.objects.create(
            total_price = data['total_price'],
            status = data['status']
        )
        return order

    def get_order(self, id):
        order = Product.objects.filter(id = id).first()
        return order

    def update_order(self, data):
        order = Order.objects.filter(id = data['id']).first()
        order.total_price = data['total_price']
        order.status = data['status']
        order.save()

    def delete_order(self, id):
        order = Order.objects.filter(id = id).first()
        order.delete()

class Order(models.Model):
    total_price = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()

class CartManager(models.Manager):
    def create_cart(self, data):
        user = User.objects.get_user(data['user_id'])
        product = Product.objects.get_product(data['product_id'])
        order = Order.objects.get_order(data['order_id'])
        cart = Cart.objects.create(
            user = user,
            product = product,
            order = order,
            quantity = data['quantity']
        )
        return cart

    def get_cart(self, id):
        cart = Cart.objects.filter(id = id).first()
        return cart

    def update_cart(self, data):
        cart = Cart.objects.filter(id = data['id']).first()
        cart.quantity = data['quantity']
        cart.save()

    def delete_cart(self, id):
        cart = Cart.objects.filter(id = id).first()
        cart.delete()

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='requests', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CartManager()
