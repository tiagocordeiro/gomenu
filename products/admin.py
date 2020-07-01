from django.contrib import admin

from .models import Product, Category, Variation, ProductVariation


class ProductVariationInLine(admin.StackedInline):
    model = ProductVariation
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')


class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'restaurant')
    inlines = [
        ProductVariationInLine,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variation, VariationAdmin)
