from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('registration',views.registration),
    path('sign_in',views.sign_in),
    path('register',views.register),
    path('success',views.success),
    path('logout',views.logout),
    path('log_in',views.log_in),
    
]