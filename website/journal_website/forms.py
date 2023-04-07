from .models import User
from django.forms import ModelForm, TextInput

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'nickname', 'password', 'email']

        widgets = {
            "first_name": TextInput(attrs={
                'placeholder': 'First name'
            }),
            "last_name": TextInput(attrs={
                'placeholder': 'Last name'
            }),
            "middle_name": TextInput(attrs={
                'placeholder': 'Middle name'
            }),
            "nickname": TextInput(attrs={
                'placeholder': 'Nickname'
            }),
            "password": TextInput(attrs={
                'placeholder': 'Password'
            }),
            "email": TextInput(attrs={
                'placeholder': 'Email'
            })
        }