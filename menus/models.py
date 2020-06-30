from django.db import models
from django.utils.text import slugify

from core.models import Active, TimeStampedModel
from restaurants.models import Restaurant


class Menu(TimeStampedModel, Active):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    slug = models.SlugField(max_length=255, verbose_name="slug",
                            help_text="Preenchido automaticamente, não editar",
                            null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
