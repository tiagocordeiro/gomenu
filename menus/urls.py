from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('new/', views.new_menu, name='new_menu'),
    path('json/<pk>/', views.menu_json, name='menu_json'),
    path('print/<pk>/', views.menu_print, name='menu_print'),
    path('qrcode/<pk>/', views.menu_qrcode_gen, name='qr_gen'),
    path('view/<pk>/<slug>/', views.menu_display, name='menu_display'),
    path('qrcode/sheet/<pk>/<size>/', views.qr_sheet_gen, name='qr_sheet_gen'),
    path('update/<pk>/', views.update_menu, name='update_menu'),
]
