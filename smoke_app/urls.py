from django.urls import path
from . import views

urlpatterns = [
    path('shisha_cat',views.shisha_cat),
    path('accessories_cat',views.accessories_cat),
    path('electronic_cat',views.electronic_cat),
    path('', views.autocomplete ,name='autocomplete'),
    path('registration',views.registration),
    path('sign_in',views.sign_in),
    path('register',views.register),
    path('success',views.success),
    path('logout',views.logout),
    path('log_in',views.log_in),

# ============================================================================
# by mohammad - link to selected product info page

    path('products/<int:id>', views.product_details),

# ============================================================================


]