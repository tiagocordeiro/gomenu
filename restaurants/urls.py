from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_restaurant, name='my_restaurant'),
    path('new/', views.new_restaurant, name='new_restaurant'),
    path('detail/<pk>/', views.restaurant_detail, name='restaurant_detail'),
]
