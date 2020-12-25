from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from .models import User, Product , Cart,Order
from django.contrib import messages
from django.utils.dateparse import parse_date
import re
import datetime

# ============================================================================
# by kamal - selected category page functionality
def shisha_cat(request):
    products = Product.objects.filter(category = 'shisha')
    context = {
        'products': products
    }
    return render(request, 'category.html', context)


def accessories_cat(request):
    products = Product.objects.filter(category = 'accessories')
    context = {
        'products': products
    }
    return render(request, 'category.html', context)
    

def electronic_cat(request):
    products = Product.objects.filter(category = 'electronics')
    context = {
        'products': products
    }
    return render(request, 'category.html', context)
    
# ============================================================================
def autocomplete(request):
    if 'term' in request.GET:
        Q = Product.objects.filter(name__istartswith=request.GET.get('term'))
        names=list()
        for product in Q :
            names.append(product.name)
        return JsonResponse(names ,safe=False)
    return render(request,"home.html")

def registration(request):
    return render(request,'registration.html')

def register(request):
    if request.method=="POST":
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # today = datetime.datetime.now().strftime("%Y%m%d")
        errors = {}
        if len(request.POST['first_name']) < 2:
            errors["first_name"] = "This name is too short"
        if len(request.POST['last_name']) < 2:
            errors["last_name"] = "This name is too short go to court and change your name"        
        if not EMAIL_REGEX.match(request.POST['email']):                
            errors['email'] = "Invalid email address!"
        if len(request.POST['password']) < 8:
            errors["password"] = "password is to short"        
        if request.POST['password']!=request.POST['confirm']:
            errors['confirm'] = "not matching!!!"
        all_users_emails = User.objects.all().values_list('email', flat=True)
        for i in all_users_emails:
            if i == request.POST['email']:
                errors['email'] = "you already registered !!"
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/registration')
        else:
            data ={   
            'first_name' : request.POST['first_name'],
            'last_name' :request.POST['last_name'],
            'email' : request.POST['email'],
            'password' : request.POST['password']
            }
            confirm = request.POST['confirm']
            if password==confirm:
                users=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password, is_admin=False)
                if 'user_id' not in request.session:
                    request.session['user_id']=users.id
                    request.session['first_name']=first_name
                    request.session['last_name']=last_name
                    return redirect("/success")
            else:
                return redirect ('/')

    # return  redirect ('/')
def sign_in(request):
    return render(request,'log_in.html')

def success(request):
    if 'user_id' in request.session:
        context={
            'user':request.session['user_id'],
            "first_name":request.session['first_name'],
            "last_name":request.session['last_name']
        }
    return render(request,'home.html',context)
    

def logout(request):
    if "user_id" in request.session:
        del request.session['user_id']
    return redirect('/')
    

def log_in(request):
    if request.method=="POST":
        user=User.objects.filter(email=request.POST['email'])
        if user:
            if 'user_id' not in request.session:
                request.session['user_id']=user[0].id
                request.session['first_name']=user[0].first_name
                request.session['last_name']=user[0].last_name
        errors={}
        if user:
            if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
                return redirect('/success')
        errors["password"] = "Wrong password or invalid!!!"        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/sign_in')

    return("/sign_in")

# ============================================================================
# by mohammad - selected product info page functionality

def product_details(request, id):
    product = Product.objects.get_product(id)
    related_products = Product.objects.filter(category = product.category)
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'product_details.html', context)

def add_to_cart(request, id):
    user = User.objects.get_user(request.session['user_id'])
    product = Product.objects.get_product(id)
    Cart.objects.create(
    user = user,
    product = product,
    order = None,
    quantity = request.POST['quantity']
    )



# ============================================================================

# ============================================================================
# by dalia -get items in cart .
def cart_items(request,id):
    # if "user_id" in request.session:
    # request.session['user_id']=1
    user=User.objects.filter(id=1)
    product = Product.objects.get(id=id)
    cart = Cart.objects.create(
        user = user,
        product = product,
        quantity = request.POST['quantity'],
        order=None
    )
    context={
        "cart":cart
    }
    # return redirect('/cart')
    return render(request, 'cart.html', context)
def cart(request):
    return render(request, 'cart.html')

# ============================================================================
# by kamal part2 insert ,update,delete
def product(request):
    products=Product.objects.all()
    context={
        "products":products
    }
    return render(request,"product.html",context)

def edit_product(request,id):
    product=Product.objects.get(id=id)
    context={
        "product":product
    }
    return render(request,'edit.html',context)
    
def update_product(request,product_id):
    if request.method=="POST":
        product=Product.objects.get(id=product_id)
        product.name=request.POST['Product_name']
        product.category=request.POST['category']
        product.price=int(request.POST['price'])
        product.description=request.POST['description']
        product.stock=int(request.POST['stock'])
        product.save()
        
    return redirect('/update')

def update(request):
    return redirect("/product")

def delete_product(request,id):
        product=Product.objects.get(id=id)
        product.delete()
        return redirect("/product")

def insert_product(request):
    if request.method=="POST":
        name=request.POST['Product_name']
        category=request.POST['category']
        price=int(request.POST['price'])
        description=request.POST['description']
        stock=int(request.POST['stock'])
        Product.objects.create(name=name,category=category,price=price,description=description,stock=stock)
    return redirect('/product')

def insert(request):
    return render(request,'insert.html')

# ============================================================================
# by kamal part2 insert ,update,delete
def orders(request):
    orders=Order.objects.all()
    context={
        'orders':orders
    }
    return render(request,'order.html',context)


























