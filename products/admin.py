from admin_ordering.admin import OrderableAdmin
from django.contrib import admin

from .models import Product, Category, Variation, ProductVariation


class ProductVariationInLine(admin.StackedInline):
    model = ProductVariation
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)


class ProductAdmin(OrderableAdmin, admin.ModelAdmin):
    # The field used for ordering. Prepend a minus for reverse
    # ordering: "-order"
    ordering_field = "order"

    # You may optionally hide the ordering field in the changelist:
    # ordering_field_hide_input = False

    # The ordering field must be included both in list_display and
    # list_editable:
    list_display = ('name', 'order', 'category', 'restaurant')
    list_editable = ["order"]

    list_filter = ('category', 'restaurant')
    inlines = [
        ProductVariationInLine,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variation, VariationAdmin)
