from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re, bcrypt
from django.http import JsonResponse

def home(request):
    if 'term' in request.GET:
        Q = Product.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for product in Q:
            names.append(product.name)
        return JsonResponse(names, safe=False)
    return render(request,'home.html')

def search(request):
    product_id = Product.objects.filter(name = request.POST['product']).first().id
    return redirect(f'products/{product_id}')

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
    request.session['is_admin'] = user.is_admin
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
    if 'user_id' not in request.session:
        return redirect('/login_form')
    Cart.objects.create_cart_item(
    user_id = request.session['user_id'],
    product_id = id,
    data = request.POST
    )
    return redirect('/cart')

def cart_items(request):
    if 'user_id' in request.session:
        items = Cart.objects.get_cart_items(request.session['user_id'])
        total_price = 0
        if items:
            for item in items:
                total_price += item.product.price * item.quantity
        context = {
            'items': items,
            'total_price': total_price
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

def control_panel(request):
    return render(request, 'control_panel.html')

def admin_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin_products.html', context)

def admin_orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'admin_orders.html', context)

def edit_product(request,id):
    product = Product.objects.get(id=id)
    context={
        "product":product
    }
    return render(request,'edit.html',context)

def delete_product(request,id):
        product=Product.objects.get(id=id)
        product.delete()
        return redirect("/admin/products")

def update_product(request,product_id):
    if request.method=="POST":
        product=Product.objects.get(id=product_id)
        product.name=request.POST['Product_name']
        product.category=request.POST['category']
        product.price=request.POST['price']
        product.description=request.POST['description']
        product.stock=request.POST['stock']
        product.save()
        
    return redirect('/update')

def update(request):
    return redirect("/admin/products")

def insert(request):
    return render(request,'insert.html')

def insert_product(request):
    if request.method=="POST":
        name=request.POST['Product_name']
        category=request.POST['category']
        price=request.POST['price']
        description=request.POST['description']
        stock=request.POST['stock']
        Product.objects.create(name=name,category=category,price=price,description=description,stock=stock)
    return redirect('/admin/products')
