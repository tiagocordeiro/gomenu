from django.forms import ModelForm, TextInput

from .models import Restaurant


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'address',
            'phone',
            'image',
        ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }
