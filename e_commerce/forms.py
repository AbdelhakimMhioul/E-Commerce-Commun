from django import forms
# from .models import Checkout


# class CheckoutForm(forms.ModelForm):
#     class Meta:
#         model = Checkout
#         fields = ['address_1', 'address_2', 'city',
#                   'state', 'zip_code', 'check_me_out']


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(max_length=300, widget=forms.Textarea)
