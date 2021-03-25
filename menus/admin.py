from django.contrib import admin

from .models import Menu, MenuCategory


class MenuCategoryInLine(admin.StackedInline):
    model = MenuCategory
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'restaurant')
    list_filter = ('restaurant',)
    inlines = [
        MenuCategoryInLine,
    ]


admin.site.register(Menu, MenuAdmin)
