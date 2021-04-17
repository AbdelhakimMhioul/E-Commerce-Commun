from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactUsForm
from math import ceil
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .decorators import seller_only, admin_only, client_only

# Create your views here.


def home(request):
    products_9 = Product.objects.order_by('-rates')[:9]
    categories = Category.objects.all()[:9]
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    numCarts = carts.count()
    if request.user.is_authenticated:
        owner = request.user
        numWishes = WishlistProduct.objects.filter(user=owner).count()
        carts = Cart.objects.filter(user=owner)
        numCarts = carts.count()
    for cart in carts:
        total_price += cart.cart_total_price()
    form = ContactUsForm()
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    else:
        group = 'SELLER'
    print(group)
    context = {'products_9': products_9, 'categories': categories, 'group': group,
               'form': form, 'numWishes': numWishes, 'numCarts': numCarts, 'total_price': total_price}
    return render(request, 'home.html', context)


@login_required
@client_only
def checkout(request):
    formCheckout = CheckoutForm()
    numWishes = WishlistProduct.objects.count()
    numCarts = Cart.objects.count()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')
    context = {'formCheckout': formCheckout,
               'numCarts': numCarts, 'numWishes': numWishes}
    return render(request, 'checkout.html', context)


@login_required
@client_only
def cart(request):
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    numCarts = carts.count()
    if request.user.is_authenticated:
        owner = request.user
        numWishes = WishlistProduct.objects.filter(user=owner).count()
        carts = Cart.objects.filter(user=owner)
        numCarts = carts.count()
    for cart in carts:
        if cart.quantity_carted <= 0:
            cart.delete()
            return redirect('cart')
        total_price += cart.cart_total_price()
    context = {'numWishes': numWishes, 'carts': carts,
               'numCarts': numCarts, 'total_price': total_price}
    return render(request, 'cart.html', context)


@login_required
@client_only
def addCart(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        try:
            cart = get_object_or_404(Cart, product=produit)
            cart.quantity_carted += 1
            cart.save()
        except:
            myCart = Cart.objects.create(
                user=request.user, product=produit, quantity_carted=1)
            myCart.save()
        numWishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        numCarts = carts.count()
        if request.user.is_authenticated:
            owner = request.user
            numWishes = WishlistProduct.objects.filter(user=owner).count()
            carts = Cart.objects.filter(user=owner)
            numCarts = carts.count()
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['total_price'] = '<div id="total" class="cart_price" >$' + \
            str(total_price) + '</div>'
        data['numCarts'] = '<div id="numCarts" class="cart_count"><span>' + \
            str(numCarts)+'</span></div>'
        return JsonResponse(data)
    return redirect('home')


@login_required
@client_only
def deleteCart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.delete()
    return redirect('cart')


@login_required
@client_only
def addWishlist(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        numWishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        numCarts = carts.count()
        if request.user.is_authenticated:
            owner = request.user
            m = WishlistProduct.objects.create(user=owner, product=produit)
            m.save()
            numWishes = WishlistProduct.objects.filter(user=owner).count()
            carts = Cart.objects.filter(user=owner)
            numCarts = carts.count()
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return render(request, 'wishlist.html')


def viewProduct(request, pk):
    numCarts = Cart.objects.count()
    product = Product.objects.get(pk=pk)
    rate_avg = ceil(product.avg_rate()*5) if product.avg_rate() >= 0 else 0
    real_rate = int(product.avg_rate()*100) if product.avg_rate() >= 0 else 0
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, 'numCarts': numCarts}
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
@client_only
def rated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.good_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


@login_required
@client_only
def unrated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.bad_rates += 1
        instance.save()
    return redirect('viewProduct', pk=pk)


@client_only
def categorie(request, pk):
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    numCarts = carts.count()
    for cart in carts:
        total_price += cart.cart_total_price()
    products = Product.objects.filter(category__pk=pk)
    paginator = Paginator(products, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products_list = paginator.page(page)
    except(Emptypage, InvalidPage):
        products_list = paginator.page(paginator.num_pages)
    context = {'products': products, 'numCarts': numCarts, 'categorie': pk,
               'numWishes': numWishes, 'total_price': total_price, 'products_list': products_list}
    return render(request, 'categorie.html', context)


@login_required
@client_only
def eliminateWish(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        wish = WishlistProduct.objects.get(pk=pk)
        wish.delete()
        carts = Cart.objects.all()
        numCarts = carts.count()
        numWishes = WishlistProduct.objects.count()
        total_price = 0
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return redirect('wishlist')


@login_required
@client_only
def wishlist(request):
    wishes = WishlistProduct.objects.all()
    numWishes = wishes.count()
    carts = Cart.objects.filter(user=request.user)
    numCarts = carts.count()
    total_price = 0
    for cart in carts:
        total_price += cart.cart_total_price()
    context = {'products': wishes, 'numWishes': numWishes,
               'numCarts': numCarts, 'total_price': total_price}
    return render(request, 'wishlist.html', context)


@client_only
def increaseQuantity(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.quantity_carted += 1
    cart.save()
    return redirect('cart')


@client_only
def decreaseQuantity(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.quantity_carted -= 1
    cart.save()
    return redirect('cart')
