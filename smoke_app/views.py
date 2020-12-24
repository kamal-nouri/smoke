from django.shortcuts import render, redirect,HttpResponse
import bcrypt
from .models import User, Product , Cart,Order
from django.contrib import messages
from django.utils.dateparse import parse_date
import re
import datetime


def shisha_cat(request):
    return render(request,'category.html')

def accessories_cat(request):
    return render(request,'category.html')

def electronic_cat(request):
    return render(request,'category.html')

def root(request):
    # if "user" in request.session:
    #     return redirect('/')
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
                if 'user' not in request.session:
                    request.session['user']=users.id
                    request.session['first_name']=first_name
                    request.session['last_name']=last_name
                    return redirect("/success")
            else:
                return redirect ('/')

    # return  redirect ('/')
def sign_in(request):
    return render(request,'log_in.html')

def success(request):
    if 'user' in request.session:
        context={
            'user':request.session['user'],
            "first_name":request.session['first_name'],
            "last_name":request.session['last_name']
        }
    return render(request,'home.html',context)
    

def logout(request):
    if "user" in request.session:
        del request.session['user']
    return redirect('/')
    

def log_in(request):
    if request.method=="POST":
        user=User.objects.filter(email=request.POST['email'])
        if user:
            if 'user' not in request.session:
                request.session['user']=user[0].id
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

# ============================================================================










































