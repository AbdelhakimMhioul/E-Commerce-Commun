from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Product


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description',
                  'photo', 'price', 'quantity', 'color']


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    adress_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control '
    }))
    adress_2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control p-0'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        })
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
