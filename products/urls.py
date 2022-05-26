from django.urls import path

from . import views

urlpatterns = [
    path('', views.products_list, name="products_list"),
    path('new/', views.product_new, name="product_new"),
    path('update/<pk>/', views.product_update, name="product_update"),
    path('delete/<pk>/', views.product_delete, name="product_delete"),
    path('sort/', views.products_sort, name="products_sort"),
    path('sort/<category>/', views.products_sort, name="products_sort"),
    path('save-products-ordering', views.save_new_ordering, name="save-products-ordering"),
    path('categories/', views.categories_list, name="categories_list"),
    path('category/new/', views.category_new, name="category_new"),
    path('category/update/<pk>/', views.category_update, name="category_update"),
    path('import/woo/<product_id>/',
         views.import_from_woocommerce,
         name="import_from_woocommerce"),
    path('import/woo/category/<category_id>/',
         views.import_all_from_woocommerce_category,
         name="import_all_from_woocommerce_category"),
]
