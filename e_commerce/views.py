from .models import Category, Product, Rating
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg
from .forms import CheckoutForm, ContactUsForm
from math import ceil

# Create your views here.


def home(request):
    products_9 = Product.objects.all()[:9]
    categories = Category.objects.all()[:9]
    form = ContactUsForm()
    context = {'products_9': products_9, 'categories': categories,
               'form': form}
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
    rating = Rating.objects.filter(
        product__pk=pk).aggregate(Avg('rates'))['rates__avg']
    rate_avg = ceil(rating) if rating is not None else 0
    real_rate = int(rating/5*100) if rating is not None else 0
    context = {'product': produit, 'rate_avg': rate_avg,
               'real_rate': real_rate, }
    return render(request, 'viewProduct.html', context)


def rated(request, pk):
    submitbutton = request.POST['Submit']
    print(submitbutton)
    if request.method == 'POST':
        if submitbutton:
            instance = get_object_or_404(Rating, product__pk=pk)
            instance.rates += 1
            instance.save()
            return viewProduct(request, pk)
    return redirect('home')


def categorie(request, categorie):
    products = Product.objects.filter(category__category=categorie)
    context = {'products': products}
    return render(request, 'categorie.html', context)
