from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=255, required=True,
                            widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ("email")
