from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderItem


class OrderItemsInLine(admin.StackedInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'customer', 'restaurant']
    inlines = [OrderItemsInLine]


admin.site.register(Order, OrderAdmin)
