from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Product, Category, ProductVariation


class ProductVariationInLine(admin.StackedInline):
    model = ProductVariation
    extra = 1


class CategoryAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)


class ProductVariationAdmin(admin.ModelAdmin):
    search_fields = ["product"]
    list_display = ('product', 'variation', 'price')
    list_filter = ('product__restaurant',)
    list_editable = ['variation', 'price']


class ProductAdmin(OrderableAdmin, admin.ModelAdmin):
    # The field used for ordering. Prepend a minus for reverse
    # ordering: "-order"
    ordering_field = "order"
    search_fields = ["name"]

    # You may optionally hide the ordering field in the changelist:
    # ordering_field_hide_input = False

    # The ordering field must be included both in list_display and
    # list_editable:
    list_display = ('name', 'price', 'product_type', 'order', 'category', 'restaurant')
    list_editable = ["order", "price"]

    list_filter = ('category', 'restaurant')
    inlines = [
        ProductVariationInLine,
    ]

    @staticmethod
    def product_type(obj):
        if len(obj.productvariation_set.all()) >= 1:
            return 'variavel'
        else:
            return 'simples'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
