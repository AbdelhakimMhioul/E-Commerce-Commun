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
    carts = Cart.objects.all()
    total_price = 0
    for cart in carts:
        total_price += cart.product.price
    numCart = Cart.objects.count()
    form = ContactUsForm()
    context = {'products_9': products_9, 'categories': categories,
               'form': form, 'numWishes': numWishes, 'numCart': numCart, 'total_price': total_price}
    return render(request, 'home.html', context)


def checkout(request):
    formCheckout = CheckoutForm()
    numCart = Cart.objects.count()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')

    context = {'formCheckout': formCheckout, 'numCart': numCart}
    return render(request, 'checkout.html', context)


def cart(request):
    numWishes = WishlistProduct.objects.count()
    numCart = Cart.objects.count()
    carts = Cart.objects.all()
    total_price = 0
    for cart in carts:
        total_price += cart.product.price
    context = {'numWishes': numWishes, 'carts': carts,
               'numCart': numCart, 'total_price': total_price}
    return render(request, 'cart.html', context)


def addCart(request, pk):
    numCart = Cart.objects.count()
    numWishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    total_price = 0
    for cart in carts:
        total_price += cart.product.price
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        Cart.objects.create(
            product=product
        )
        return redirect('home')
    return render(request, 'cart.html', {'numCart': numCart, 'numWishes': numWishes, 'total_price': total_price})


def eliminateCart(request, pk):
    wish = Cart.objects.get(pk=pk)
    wish.delete()
    return redirect('cart')


def viewProduct(request, pk):
    numCart = Cart.objects.count()
    product = Product.objects.get(pk=pk)
    avg_bad_rates = Product.objects.filter(
        pk=pk).aggregate(Avg('bad_rates'))['bad_rates__avg']
    avg_good_rates = Product.objects.filter(
        pk=pk).aggregate(Avg('good_rates'))['good_rates__avg']
    rate = (product.good_rates-product.bad_rates)/(product.bad_rates+product.good_rates)
    rate_avg = ceil(rate)
    real_rate = int(rate*100)
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, 'numCart': numCart}
    return render(request, 'viewProduct.html', context)


def rated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.good_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


def unrated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.bad_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


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
    numCart = Cart.objects.count()
    products = WishlistProduct.objects.all()
    carts = Cart.objects.all()
    total_price = 0
    for cart in carts:
        total_price += cart.product.price
    context = {'products': products,
               'numWishes': numWishes, 'numCart': numCart, 'total_price': total_price}
    return render(request, 'wishlist.html', context)


def increaseQuantity(request):
    pass


def decreaseQuantity(request):
    pass
