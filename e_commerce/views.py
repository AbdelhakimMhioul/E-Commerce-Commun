from products.models import Product
from django.shortcuts import render

# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)
