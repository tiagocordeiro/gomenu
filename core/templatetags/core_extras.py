import locale

from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        return user.groups.filter(name=group_name).exists()
    except AttributeError:
        return False


@register.filter(name='subtotal')
def subtotal(unity_price, quantity):
    return unity_price * quantity


@register.filter(name='currency_display')
def currency_display(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    value = locale.currency(value, grouping=True, symbol=None)
    return value
