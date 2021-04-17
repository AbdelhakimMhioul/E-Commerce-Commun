from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Seller, Client

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


# class ClientSignUpForm(UserCreationForm):
#     class Meta:
#         model = Client
#         fields = "__all__"

#     def save(self, commit=True):
#         client = super(ClientSignUpForm, self).save(commit=False)
#         client.name = self.cleaned_data['name']
#         client.email = self.cleaned_data['email']
#         if commit:
#             client.save()
#         return client


# class SellerSignUpForm(UserCreationForm):
#     class Meta:
#         model = Seller
#         fields = '__all__'
#         exclude = ['user']


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ("email")
