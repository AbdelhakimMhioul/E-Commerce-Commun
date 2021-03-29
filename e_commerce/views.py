from products.models import Category, Product, SuperCategory
from django.shortcuts import render

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    superCategories = SuperCategory.objects.all()
    context = {'products': products, 'categories': categories,
               'superCategories': superCategories}
    return render(request, 'home.html', context)
