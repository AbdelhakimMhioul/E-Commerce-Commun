from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CheckoutForm, ContactUsForm
from math import ceil
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    products_9 = Product.objects.order_by('-rates')[:9]
    categories = Category.objects.all()[:9]
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    orders = Order.objects.all()
    numOrders = orders.count()
    if request.user.is_authenticated:
        owner = request.user
        numWishes = WishlistProduct.objects.filter(user=owner).count()
        orders = Order.objects.filter(user=owner)
        numOrders = orders.count()
    for order in orders:
        total_price += order.order_total_price()
    form = ContactUsForm()
    context = {'products_9': products_9, 'categories': categories,
               'form': form, 'numWishes': numWishes, 'numOrders': numOrders, 'total_price': total_price}
    return render(request, 'home.html', context)


@login_required
def checkout(request):
    formCheckout = CheckoutForm()
    numWishes = WishlistProduct.objects.count()
    numOrders = Order.objects.count()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')
    context = {'formCheckout': formCheckout,
               'numOrders': numOrders, 'numWishes': numWishes}
    return render(request, 'checkout.html', context)


@login_required
def cart(request):
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    orders = Order.objects.all()
    numOrders = orders.count()
    if request.user.is_authenticated:
        owner = request.user
        numWishes = WishlistProduct.objects.filter(user=owner).count()
        orders = Order.objects.filter(user=owner)
        numOrders = orders.count()
    for order in orders:
        if order.quantity_ordered <= 0:
            order.delete()
            return redirect('cart')
        total_price += order.order_total_price()
    context = {'numWishes': numWishes, 'orders': orders,
               'numOrders': numOrders, 'total_price': total_price}
    return render(request, 'cart.html', context)


@login_required
def addCart(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        try:
            order = get_object_or_404(Order, product=produit)
            order.quantity_ordered += 1
            order.save()
        except:
            myOrder = Order.objects.create(
                user=request.user, product=produit, quantity_ordered=1)
            myOrder.save()
        numWishes = WishlistProduct.objects.count()
        orders = Order.objects.all()
        numOrders = orders.count()
        if request.user.is_authenticated:
            owner = request.user
            numWishes = WishlistProduct.objects.filter(user=owner).count()
            orders = Order.objects.filter(user=owner)
            numOrders = orders.count()
        for order in orders:
            total_price += order.order_total_price()
        data = {}
        data['total_price'] = '<div id="total" class="cart_price" >$' + \
            str(total_price) + '</div>'
        data['numOrders'] = '<div id="numOrders" class="cart_count"><span>' + \
            str(numOrders)+'</span></div>'
        return JsonResponse(data)
    return redirect('home')


@login_required
def deleteOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('cart')


@login_required
def addWishlist(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        numWishes = WishlistProduct.objects.count()
        orders = Order.objects.all()
        numOrders = orders.count()
        if request.user.is_authenticated:
            owner = request.user
            m = WishlistProduct.objects.create(user=owner, product=produit)
            m.save()
            numWishes = WishlistProduct.objects.filter(user=owner).count()
            orders = Order.objects.filter(user=owner)
            numOrders = orders.count()
        for order in orders:
            total_price += order.order_total_price()
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return render(request, 'wishlist.html')


def viewProduct(request, pk):
    numOrders = Order.objects.count()
    product = Product.objects.get(pk=pk)
    rate_avg = ceil(product.avg_rate()*5) if product.avg_rate() >= 0 else 0
    real_rate = int(product.avg_rate()*100) if product.avg_rate() >= 0 else 0
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, 'numOrders': numOrders}
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
    total_price = 0
    numWishes = WishlistProduct.objects.count()
    orders = Order.objects.all()
    numOrders = orders.count()
    for order in orders:
        total_price += order.order_total_price()
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
    context = {'products': products, 'numOrders': numOrders, 'categorie': pk,
               'numWishes': numWishes, 'total_price': total_price, 'products_list': products_list}
    return render(request, 'categorie.html', context)


@login_required
def eliminateWish(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        wish = WishlistProduct.objects.get(pk=pk)
        wish.delete()
        orders = Order.objects.all()
        numOrders = orders.count()
        numWishes = WishlistProduct.objects.count()
        total_price = 0
        for order in orders:
            total_price += order.order_total_price()
        data = {}
        data['numWishes'] = '<div id="numWishes" class="wishlist_count">' + \
            str(numWishes)+'</div>'
        return JsonResponse(data)
    return redirect('wishlist')


@login_required
def wishlist(request):
    wishes = WishlistProduct.objects.all()
    numWishes = wishes.count()
    orders = Order.objects.filter(user=request.user)
    numOrders = orders.count()
    total_price = 0
    for order in orders:
        total_price += order.order_total_price()
    context = {'products': wishes, 'numWishes': numWishes,
               'numOrders': numOrders, 'total_price': total_price}
    return render(request, 'wishlist.html', context)


def increaseQuantity(request, pk):
    order = Order.objects.get(pk=pk)
    order.quantity_ordered += 1
    order.save()
    return redirect('cart')


def decreaseQuantity(request, pk):
    order = Order.objects.get(pk=pk)
    order.quantity_ordered -= 1
    order.save()
    return redirect('cart')



