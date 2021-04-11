from .models import *
from django.shortcuts import render, redirect
from .forms import CheckoutForm, ContactUsForm
from math import ceil
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    products_9 = Product.objects.all().order_by('-rates')[:9]
    categories = Category.objects.all()[:9]
    numWishes = WishlistProduct.objects.count()
    numCart = Cart.objects.count()
    carts = Cart.objects.all()
    total_price = 0
    for cart in carts:
        total_price += cart.product.price
    form = ContactUsForm()
    context = {'products_9': products_9, 'categories': categories,
               'form': form, 'numWishes': numWishes, 'numCart': numCart, 'total_price': total_price}
    return render(request, 'home.html', context)


@login_required
def checkout(request):
    formCheckout = CheckoutForm()
    numWishes = WishlistProduct.objects.count()
    numCart = Cart.objects.count()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')

    context = {'formCheckout': formCheckout,
               'numCart': numCart, 'numWishes': numWishes}
    return render(request, 'checkout.html', context)


@login_required
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


@login_required
def addCart(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        m = Cart(product=produit)
        m.save()
        numCart = Cart.objects.count()
        numWishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        total_price = 0
        for cart in carts:
            total_price += cart.product.price
        data = {}
        data['total_price'] = '<div id="total" class="cart_price" >$' + \
            str(total_price) + '</div>'
        data['numCart'] = '<div id="numCart" class="cart_count"><span>' + \
            str(numCart)+'</span></div>'
        return JsonResponse(data)
    return redirect('home')


@login_required
def addWishlist(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        m = WishlistProduct(product=produit)
        m.save()
        numCart = Cart.objects.count()
        numWishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        total_price = 0
        for cart in carts:
            total_price += cart.product.price
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return render(request, 'wishlist.html', {'numCart': numCart, 'numWishes': numWishes, 'total_price': total_price})


@login_required
def eliminateCart(request, pk):
    wish = Cart.objects.get(pk=pk)
    wish.delete()
    return redirect('cart')


def viewProduct(request, pk):
    numCart = Cart.objects.count()
    product = Product.objects.get(pk=pk)
    rate_avg = ceil(product.avg_rate()*5) if product.avg_rate() >= 0 else 0
    real_rate = int(product.avg_rate()*100) if product.avg_rate() >= 0 else 0
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, 'numCart': numCart}
    return render(request, 'viewProduct.html', context)


def search_form(request):
    if 'term' in request.GET and request.GET['term']:
        term = request.GET.get('term')
        qs = Product.objects.filter(name__startswith=term)
        sources = []
        for product in qs:
            sources.append(
                {"value": "/view-product/"+str(product.id)+"/", "label": product.name})
        return JsonResponse(sources, safe=False)
    if 'search' in request.GET and request.GET['search']:
        search_query = request.GET.get('search')
        products = Product.objects.filter(
            Q(name__contains=search_query) | Q(category__category__contains=search_query) | Q(description__contains=search_query)).order_by('-rates')
    else:
        products = Product.objects.all().order_by('-rates')
    return render(request, 'searches.html', {'products': products})


@login_required
def rated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.good_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


@login_required
def unrated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.bad_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


def categorie(request, pk):
    numWishes = WishlistProduct.objects.count()
    numCart = Cart.objects.count()
    total_price = 0
    carts = Cart.objects.all()
    for cart in carts:
        total_price += cart.product.price
    products = Product.objects.filter(category__pk=pk)
    context = {'products': products, 'numCart': numCart, 'categorie': pk,
               'numWishes': numWishes, 'total_price': total_price}
    return render(request, 'categorie.html', context)


@login_required
def eliminateWish(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        wish = WishlistProduct.objects.get(pk=pk)
        wish.delete()
        numCart = Cart.objects.count()
        numWishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        total_price = 0
        for cart in carts:
            total_price += cart.product.price
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return redirect('wishlist')


@login_required
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
