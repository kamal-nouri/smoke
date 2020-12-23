from django.shortcuts import render, redirect

def index(request):
    return render(request, 'home.html')


def shisha_cat(request):
    return render(request,'category.html')

def accessories_cat(request):
    return render(request,'category.html')

def electronic_cat(request):
    return render(request,'category.html')






