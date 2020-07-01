from django.contrib import admin

from restaurants.models import Restaurant, RestaurantIntegrations


class RestauratnIntegrationsInLine(admin.StackedInline):
    model = RestaurantIntegrations
    extra = 1
    max_num = 1


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager')
    inlines = [
        RestauratnIntegrationsInLine
    ]


admin.site.register(Restaurant, RestaurantAdmin)
