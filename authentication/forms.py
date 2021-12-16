from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """ Form for django-admin page, create user"""
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """ Form for django-admin page, customize user"""
    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')
