from django.contrib import admin

from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')


admin.site.register(Menu, MenuAdmin)
