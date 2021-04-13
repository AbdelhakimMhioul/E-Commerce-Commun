from django.forms import ModelForm
from e_commerce.models import Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description','photo','price','quantity']
