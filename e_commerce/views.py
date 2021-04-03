from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg
from .forms import CheckoutForm, ContactUsForm
from math import ceil

# Create your views here.


def home(request):
    products_9 = Product.objects.all().order_by('-rates')[:9]
    categories = Category.objects.all()[:9]
    numWishes = WishlistProduct.objects.count()
    form = ContactUsForm()
    context = {'products_9': products_9, 'categories': categories,
               'form': form, 'numWishes': numWishes}
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
    product = Product.objects.get(pk=pk)
    rating = Product.objects.filter(
        pk=pk).aggregate(Avg('rates'))['rates__avg']
    rate_avg = ceil(rating) if rating is not None else 0
    real_rate = int(rating/5*100) if rating is not None else 0
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, }
    return render(request, 'viewProduct.html', context)


def rated(request, pk):
    submitbutton = request.POST['Submit']
    if request.method == 'POST':
        if submitbutton:
            instance = get_object_or_404(Product, pk=pk)
            instance.rates += 1
            instance.save()
            return viewProduct(request, pk)
    return redirect('home')


def categorie(request, categorie):
    products = Product.objects.filter(category__category=categorie)
    context = {'products': products}
    return render(request, 'categorie.html', context)


def addWishlist(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        WishlistProduct.objects.create(
            product=product
        )
        return redirect('home')
    return render(request, 'wishlist.html')


def eliminateWish(request, pk):
    wish = WishlistProduct.objects.get(pk=pk)
    wish.delete()
    return redirect('wishlist')


def wishlist(request):
    numWishes = WishlistProduct.objects.count()
    products = WishlistProduct.objects.all()
    context = {'products': products, 'numWishes': numWishes}
    return render(request, 'wishlist.html', context)
