from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re, bcrypt

def home(request):
    return render(request,'home.html')

def regist_form(request):
    return render(request,'regist_form.html')

def register_validator(data):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not len(data['first_name']) >= 2:
        errors['first_name'] = 'First Name Required! at least 2 characters'
    if not len(data['last_name']) >= 2:
        errors['last_name'] = 'Last Name Required! at least 2 characters'
    if not EMAIL_REGEX.match(data['email']):
        errors['email'] = 'Invalid email format!'
    if len(User.objects.filter(email = data['email'])):
        errors['email'] = 'Email address already exists!'
    if not len(data['password']) >= 8:
        errors['password'] = 'Password Required! at least 8 characters'
    if not data['pw_confirm'] == data['password']:
        errors['pw_confirm'] = 'Password does not match!'
    return errors

def register(request):
    errors = register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regist_form')
    User.objects.create_user(request.POST)
    messages.success(request, 'Congratulations! you have successfully registered')
    return redirect('/login_form')

def login_form(request):
    return render(request,'login_form.html')

def login_validator(data):
    errors = {}
    user = User.objects.filter(email = data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode(), user.password.encode()):
        return errors
    errors['login'] = 'Invalid email or password!'
    return errors

def login(request):
    errors = login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_form')
    if 'user_id' in request.session:
        return redirect('/')
    user = User.objects.filter(email = request.POST['email']).first()
    request.session['user_id'] = user.id
    return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

def cat_items(request, category):
    products = Product.objects.filter(category = category)
    context = {
        'category': category.upper(),
        'products': products
    }
    return render(request, 'cat_items.html', context)

def product_info(request, id):
    product = Product.objects.get_product(id)
    related_products = Product.objects.filter(category = product.category)
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'product_info.html', context)

def add_to_cart(request, id):
    Cart.objects.create_cart_item(
    user_id = request.session['user_id'],
    product_id = id,
    data = request.POST
    )
    return redirect('/cart')

def cart_items(request):
    if 'user_id' in request.session:
        items = Cart.objects.get_cart_items(request.session['user_id'])
        context = {
            'items': items
        }
        return render(request, 'cart_items.html', context)

def remove_from_cart(request, id):
    Cart.objects.delete_cart_item(id)
    return redirect('/cart')

def purchase(request):
    errors = {}
    if 'user_id' not in request.session:
        messages.error(request, 'You need to login first!')
        return redirect('/cart')
    order = Order.objects.create_order(request.session['user_id'])
    if not order:
        messages.error(request, 'You have nothing in the cart!')
        return redirect('/cart')
    messages.success(request, 'Your purchase has successfully ordered!')
    return redirect('/cart')
