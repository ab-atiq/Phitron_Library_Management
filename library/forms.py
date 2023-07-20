from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(BaseUserCreationForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        model = User
