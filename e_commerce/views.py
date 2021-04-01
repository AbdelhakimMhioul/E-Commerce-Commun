from .models import Category, Product, Rating
from django.shortcuts import render, redirect
from django.db.models import Avg
from .forms import CheckoutForm
from math import ceil
from .forms import FormContactUs

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    form =FormContactUs
    if request.method == 'POST':
        form = FormContactUs(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'products': products, 'categories': categories, 'form':form }
    return render(request, 'home.html', context)


def checkout(request):
    formCheckout = CheckoutForm()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')

    context = {'formCheckout': formCheckout}
    return render(request, 'checkout.html', context)


def cart(request):
    return render(request, 'cart.html', {})


def viewProduct(request, pk):
    produit = Product.objects.get(pk=pk)
    rate_avg = ceil(Rating.objects.filter(
        product__pk=pk).aggregate(Avg('rates'))['rates__avg'])
    context = {'product': produit, 'rate_avg': rate_avg}
    return render(request, 'viewProduct.html', context)

