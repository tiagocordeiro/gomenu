from django.db import models

from core.models import TimeStampedModel, Active
from restaurants.models import Restaurant


class Category(TimeStampedModel, Active):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField("Categoria", max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("name",)
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class Product(TimeStampedModel, Active):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=100)
    description = models.TextField("Descrição", blank=True)
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField('ordem', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class ProductVariation(TimeStampedModel, Active):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.CharField("Variação", max_length=100, null=True)
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)

    def __str__(self):
        return str(
            self.product.name
            + " - "
            + self.variation
            + " - "
            + self.price.__str__()
        )

    class Meta:
        ordering = ("product", "price", "variation")
        unique_together = [("product", "variation")]
