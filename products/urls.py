from django.urls import path

from . import views

urlpatterns = [
    path('', views.products_list, name="products_list"),
    path('categories/', views.categories_list, name="categories_list"),
    path('category/new/', views.category_new, name="category_new"),
]
