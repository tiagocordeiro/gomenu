import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import Active, TimeStampedModel
from products.models import Product, Variation
from restaurants.models import Restaurant


def gen_uuid():
    return str(uuid.uuid4())


class Order(Active, TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', "Pendente"),
        ('processing', "Processando"),
        ('on_hold', "Aguardando"),
        ('shipped', "Enviado"),
        ('complete', "Concluido"),
        ('canceled', "Cancelado"),
    )
    slug = models.UUIDField(unique=True, editable=False)
    notes = models.TextField('observações', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name='restaurante',
                                   on_delete=models.CASCADE)
    customer = models.ForeignKey(User, verbose_name='cliente',
                                 on_delete=models.CASCADE, blank=True,
                                 null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending',
                              max_length=20)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = gen_uuid()
            super(Order, self).save(*args, **kwargs)
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE,
                                  blank=True, null=True)
    notes = models.TextField('observações', blank=True, null=True)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    unity_price = models.DecimalField('Valor unitário', max_digits=10,
                                      decimal_places=2, null=True, blank=True)
