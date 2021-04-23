from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .components.cart import *
from .components.checkout import *
from .components.wishlist import *
from .components.view_product import *
from .components.rate import *
from .filters import ProductFilter


def my_groups():
    if Group.objects.exists():
        return
    g0 = Group.objects.create(name='ADMIN')
    g1 = Group.objects.create(name='CLIENT')
    g2 = Group.objects.create(name='SELLER')
    User = get_user_model()
    if User.objects.exists():
        return
    admin = User.objects.create_superuser(
        'admin', 'admin@myproject.com', 'password')
    g0.user_set.add(admin)


def home(request):
    my_groups()
    products = Product.objects.all()
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
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    if request.method == 'GET':
        myFilter = ProductFilter(request.GET, queryset=products)
        products_9 = myFilter.qs.order_by('-rates')[:9]
    context = {'products_9': products_9, 'categories': categories, 'group': group, 'myFilter': myFilter,
               'num_wishes': num_wishes, 'num_carts': num_carts, 'total_price': total_price}
    return render(request, 'home.html', context)
