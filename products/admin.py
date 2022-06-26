from admin_ordering.admin import OrderableAdmin
from django.contrib import admin

from .models import Product, Category, ProductVariation


class CategoryFilter(admin.SimpleListFilter):
    title = 'categoria'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        if 'restaurant__id__exact' in request.GET:
            restaurant_id = request.GET['restaurant__id__exact']
            categorias = set([c.category for c in model_admin.model.objects.all().filter(restaurant=restaurant_id)])
        else:
            categorias = set([c.category for c in model_admin.model.objects.all()])
        return [(b.id, b.name) for b in categorias]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())


class ProductVariationInLine(admin.StackedInline):
    model = ProductVariation
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)


class ProductVariationAdmin(admin.ModelAdmin):
    search_fields = ["product"]
    list_display = ('product', 'variation', 'price')
    list_filter = ('product__restaurant', 'product__category')
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

    list_filter = ('restaurant', CategoryFilter)
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
