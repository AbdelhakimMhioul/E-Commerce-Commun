from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *
from .forms import ContactUsForm
from accounts.decorators import allowed_users

from math import ceil

# Create your views here.


def home(request):
    products_9 = Product.objects.order_by('-rates')[:9]
    categories = Category.objects.all()[:9]
    total_price = 0
    num_wishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    num_carts = carts.count()
    if request.user.is_authenticated:
        owner = request.user
        num_wishes = WishlistProduct.objects.filter(user=owner).count()
        carts = Cart.objects.filter(user=owner)
        num_carts = carts.count()
    for cart in carts:
        total_price += cart.cart_total_price()
    form = ContactUsForm()
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    context = {'products_9': products_9, 'categories': categories, 'group': group,
               'form': form, 'num_wishes': num_wishes, 'num_carts': num_carts, 'total_price': total_price}
    return render(request, 'home.html', context)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def checkout(request):
    form_checkout = CheckoutForm()
    num_wishes = WishlistProduct.objects.count()
    num_carts = Cart.objects.count()
    if request.method == 'POST':
        form_checkout = CheckoutForm(request.POST)
        if form_checkout.is_valid():
            form_checkout.save()
            return redirect('home')
    context = {'form_checkout': form_checkout,
               'num_carts': num_carts, 'num_wishes': num_wishes}
    return render(request, 'checkout.html', context)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def cart(request):
    total_price = 0
    num_wishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    num_carts = carts.count()
    if request.user.is_authenticated:
        owner = request.user
        num_wishes = WishlistProduct.objects.filter(user=owner).count()
        carts = Cart.objects.filter(user=owner)
        num_carts = carts.count()
    for cart in carts:
        if cart.quantity_carted <= 0:
            cart.delete()
            return redirect('cart')
        total_price += cart.cart_total_price()
    context = {'num_wishes': num_wishes, 'carts': carts,
               'num_carts': num_carts, 'total_price': total_price}
    return render(request, 'cart.html', context)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def add_cart(request, pk):
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
        num_wishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        num_carts = carts.count()
        if request.user.is_authenticated:
            owner = request.user
            num_wishes = WishlistProduct.objects.filter(user=owner).count()
            carts = Cart.objects.filter(user=owner)
            num_carts = carts.count()
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['total_price'] = '<div id="total" class="cart_price" >$' + \
            str(total_price) + '</div>'
        data['num_carts'] = '<div id="num_carts" class="cart_count"><span>' + \
            str(num_carts)+'</span></div>'
        return JsonResponse(data)
    return redirect('home')


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def delete_cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.delete()
    return redirect('cart')


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def add_wishlist(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        num_wishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        num_carts = carts.count()
        if request.user.is_authenticated:
            owner = request.user
            m = WishlistProduct.objects.create(user=owner, product=produit)
            m.save()
            num_wishes = WishlistProduct.objects.filter(user=owner).count()
            carts = Cart.objects.filter(user=owner)
            num_carts = carts.count()
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['num_wishes'] = '<div id="num_wishes" class="wishlist_count">' + \
            str(num_wishes)+'</div>'
        return JsonResponse(data)
    return render(request, 'wishlist.html')

@allowed_users(allowed_roles=['CLIENT'])
def view_product(request, pk):
    num_carts = Cart.objects.count()
    product = Product.objects.get(pk=pk)
    rate_avg = ceil(product.avg_rate()*5) if product.avg_rate() >= 0 else 0
    real_rate = int(product.avg_rate()*100) if product.avg_rate() >= 0 else 0
    context = {'product': product, 'rate_avg': rate_avg,
               'real_rate': real_rate, 'num_carts': num_carts}
    return render(request, 'view_product.html', context)


def search_form(request):
    if 'term' in request.GET and request.GET['term']:
        term = request.GET.get('term')
        qs = Product.objects.filter(name__startswith=term)
        sources = []
        for product in qs:
            sources.append(
                {"value": "/view_product/"+str(product.id)+"/", "label": product.name})
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
    return redirect('view_product', pk=pk)


@login_required
def unrated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.method == 'POST':
        instance.bad_rates += 1
        instance.save()
    return redirect('view_product', pk=pk)


@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def categorie(request, pk):
    total_price = 0
    num_wishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    num_carts = carts.count()
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
    context = {'products': products, 'num_carts': num_carts, 'categorie': pk,
               'num_wishes': num_wishes, 'total_price': total_price, 'products_list': products_list}
    return render(request, 'categorie.html', context)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def eliminate_wish(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        wish = WishlistProduct.objects.get(pk=pk)
        wish.delete()
        carts = Cart.objects.all()
        num_carts = carts.count()
        num_wishes = WishlistProduct.objects.count()
        total_price = 0
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['num_wishes'] = '<div id="num_wishes" class="wishlist_count">' + \
            str(num_wishes)+'</div>'
        return JsonResponse(data)
    return redirect('wishlist')


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def wishlist(request):
    wishes = WishlistProduct.objects.all()
    num_wishes = wishes.count()
    carts = Cart.objects.filter(user=request.user)
    num_carts = carts.count()
    total_price = 0
    for cart in carts:
        total_price += cart.cart_total_price()
    context = {'products': wishes, 'num_wishes': num_wishes,
               'num_carts': num_carts, 'total_price': total_price}
    return render(request, 'wishlist.html', context)


@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def increase_quantity(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.quantity_carted += 1
    cart.save()
    return redirect('cart')


@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def decrease_quantity(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.quantity_carted -= 1
    cart.save()
    return redirect('cart')
