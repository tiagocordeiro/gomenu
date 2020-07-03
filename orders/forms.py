from django.forms import ModelForm, NumberInput, Textarea

from .models import Order, OrderItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['notes']
        widgets = {
            'notes': Textarea(attrs={'class': 'form-control'}),
        }


class OrderItemsForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
        widgets = {
            'quantity': NumberInput(attrs={'class': 'form-control'}),
        }
