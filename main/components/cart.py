from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import allowed_users
from django.http import JsonResponse
from ..models import *


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
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    context = {'num_wishes': num_wishes, 'carts': carts, 'group': group,
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
