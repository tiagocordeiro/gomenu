from django.contrib import admin

from restaurants.models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager')


admin.site.register(Restaurant, RestaurantAdmin)
