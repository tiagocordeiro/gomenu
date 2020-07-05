from django.urls import path

from . import views

urlpatterns = [
    path('add/<int:pk>/<int:restaurant_pk>/<int:menu_pk>/',
         views.order_add_item, name='order_add_item'),
    path('add/var/<int:pk>/<int:var_pk>/<int:restaurant_pk>/<int:menu_pk>/',
         views.order_add_var_item, name='order_add_var_item'),
    path('cart/', views.cart, name='cart'),
    path('cart/<slug>/', views.cart, name='cart'),
    path('checkout/<slug>/', views.checkout, name='checkout'),
    path('detail/<slug>/', views.order_detail, name='order_detail'),
    path('list/', views.orders_list, name='orders_list'),
]
