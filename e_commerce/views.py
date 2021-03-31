from .models import Category, Product
from django.shortcuts import render

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, }
    return render(request, 'home.html', context)
