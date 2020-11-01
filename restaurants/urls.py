from django.urls import path

from . import views

urlpatterns = [
    path('restaurant/', views.my_restaurant, name='my_restaurant'),
    path('restaurant/new/', views.new_restaurant, name='new_restaurant'),
    path('restaurant/detail/<pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('<slug>/', views.restaurant_main, name='restaurant_main'),
    path('<restaurant_slug>/<menu_slug>/', views.restaurant_menu, name='restaurant_menu'),
]
