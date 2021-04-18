from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.db import transaction

USERS = (
    ('SELLER', 'SELLER'),
    ('CLIENT', 'CLIENT'),
    ('BOTH', 'BOTH'),
)


class CreateUserForm(UserCreationForm):
    choice = forms.ChoiceField(
        label="Enter Your Choice", choices=USERS, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'choice']


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ("email")
