from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, CharField, \
    EmailField

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


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False,
                           help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254,
                       help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2',)
