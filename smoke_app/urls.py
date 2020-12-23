from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('registration',views.registration),
    path('sign_in',views.sign_in),
    path('register',views.register),
    path('success',views.success),
    path('delete',views.delete),
    path('log_in',views.log_in),
    
]