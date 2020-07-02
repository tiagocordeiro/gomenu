from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    phone = models.CharField('Telefone', max_length=20)
    image = models.ImageField(upload_to='restautant/', blank=True, null=True)
    manager = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    online_sales = models.BooleanField("Vendas online", default=False)

    def __str__(self):
        return str(self.name)


class RestaurantIntegrations(models.Model):
    restaurat = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    wc_consumer_key = models.CharField(max_length=50)
    wc_consumer_secret = models.CharField(max_length=50)
    woo_commerce_url = models.URLField()
