from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import Active, TimeStampedModel
from products.models import Category
from restaurants.models import Restaurant


class Menu(TimeStampedModel, Active):
    VARIATIONS_DISPLAY_STYLE_CHOICES = [
        (1, 'Mini card'),
        (2, 'List'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    slug = models.SlugField(max_length=255, verbose_name="slug",
                            help_text="Preenchido automaticamente, não editar",
                            null=True, blank=True)
    variations_display_style = models.IntegerField(choices=VARIATIONS_DISPLAY_STYLE_CHOICES, default=1)
    dark_mode = models.BooleanField('Dark Mode', default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('restaurant_main', kwargs={'slug': self.restaurant.slug})

    def __str__(self):
        return str(self.name)


class MenuCategory(TimeStampedModel, Active):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField('ordem')
    show_in_menu = models.BooleanField(default=True)

    def __str__(self):
        return str(self.category.name + ' - ' + self.menu.name)

    class Meta:
        ordering = ('order',)
        unique_together = [("menu", "category")]
