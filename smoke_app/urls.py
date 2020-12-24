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
    path('product',views.product),
    path('edit_product/<id>',views.edit_product),
    path('update_product/<product_id>',views.update_product),
    path('update',views.update),
    path('delete_product/<id>',views.delete_product),
    path('insert_product',views.insert_product),
    path('insert',views.insert),

# ============================================================================
# by mohammad - link to selected product info page

    path('products/<int:id>', views.product_details),
    path('add_to_cart/<int:id>', views.add_to_cart),

# ============================================================================



]