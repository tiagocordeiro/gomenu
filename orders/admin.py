from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderItem


class OrderItemsInLine(admin.StackedInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'customer', 'restaurant', 'slug', 'created']
    list_filter = ('restaurant', 'status')
    inlines = [OrderItemsInLine]


admin.site.register(Order, OrderAdmin)
