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
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    total_price = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='requests', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
