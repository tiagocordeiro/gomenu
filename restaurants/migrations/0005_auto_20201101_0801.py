# Generated by Django 3.1.2 on 2020-11-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_restaurant_online_sales'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ('name',), 'verbose_name': 'restaurante', 'verbose_name_plural': 'restaurantes'},
        ),
        migrations.AddField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(blank=True, help_text='Preenchido automaticamente, não editar.', max_length=255, null=True, unique=True, verbose_name='slug'),
        ),
    ]
