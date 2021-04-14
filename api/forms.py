from django.forms import ModelForm
from e_commerce.models import Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
