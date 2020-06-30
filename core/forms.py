from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

        fields = ['avatar', ]


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }
