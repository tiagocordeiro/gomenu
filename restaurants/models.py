from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Restaurant(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    phone = models.CharField('Telefone', max_length=20)
    image = models.ImageField(upload_to='restautant/', blank=True, null=True)
    manager = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    online_sales = models.BooleanField("Vendas online", default=False)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="slug",
                            help_text="Preenchido automaticamente, não editar.",
                            null=True,
                            blank=True, )

    class Meta:
        ordering = ('name',)
        verbose_name = 'restaurante'
        verbose_name_plural = 'restaurantes'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class RestaurantIntegrations(models.Model):
    restaurat = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    wc_consumer_key = models.CharField(max_length=50)
    wc_consumer_secret = models.CharField(max_length=50)
    woo_commerce_url = models.URLField()
