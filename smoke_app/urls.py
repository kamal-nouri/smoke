from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shisha_cat',views.shisha_cat),
    path('accessories_cat',views.accessories_cat),
    path('electronic_cat',views.electronic_cat),
]