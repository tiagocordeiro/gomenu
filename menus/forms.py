from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, CheckboxInput

from .models import Menu, MenuCategory


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'variations_display_style',
            'dark_mode',
        ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'variations_display_style': Select(attrs={'class': 'form-control'}),
            'dark_mode': CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MenuCategoriesForm(ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['menu', 'category', 'order']

        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'order': NumberInput(attrs={'class': 'form-control'}),
        }
