from django import forms

from .models import Product


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(max_length=300, widget=forms.Textarea)
