from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('search', views.search),
    path('regist_form', views.regist_form),
    path('register', views.register),
    path('login_form', views.login_form),
    path('login', views.login),
    path('logout', views.logout),
    path('categories/<category>', views.cat_items),
    path('products/<int:id>', views.product_info),
    path('add_to_cart/<int:id>', views.add_to_cart),
    path('cart', views.cart_items),
    path('cart/<int:id>/delete', views.remove_from_cart),
    path('cart/order', views.purchase),
    path('control_panel', views.control_panel),
    path('admin/products', views.admin_products),
    path('admin/orders', views.admin_orders),
    path('edit_product/<id>',views.edit_product),
    path('update_product/<product_id>',views.update_product),
    path('update',views.update),
    path('delete_product/<id>',views.delete_product),
    path('insert', views.insert),
    path('insert_product',views.insert_product),

]
