from django.forms import ModelForm
from .models import Productt

class FormProduct(ModelForm):
    class Meta:
        model=Productt
        fields= '__all__'