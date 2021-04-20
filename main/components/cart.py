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
def addToCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    produit = Product.objects.get(id=productId)
    total_price = 0
    if action == 'add':
        try:
            cart = Cart.objects.get(product=produit, user=request.user)
            cart.quantity_carted += 1
        except:
            cart = Cart.objects.create(
                user=request.user, product=produit, quantity_carted=1)
        cart.save()
        if request.user.is_authenticated:
            numWishes = WishlistProduct.objects.filter(
                user=request.user).count()
            carts = Cart.objects.filter(user=request.user)
            numOrders = carts.count()
            for cart in carts:
                total_price += cart.cart_total_price()
        print(productId)
        print(action)
    return JsonResponse("added", safe=False)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def delete_cart(request, pk):
    if request.method == 'GET':
        cart_id = request.GET['cartid']
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.delete()
        carts = Cart.objects.all()
        num_carts = carts.count()
        num_wishes = WishlistProduct.objects.count()
        total_price = 0
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['total_price'] = '<div id="total" class="cart_price" >$' + \
            str(total_price) + '</div>'
        data['num_carts'] = '<div id="num_carts" class="cart_count"><span>' + \
            str(num_carts)+'</span></div>'
        data['num_wishes'] = '<div id="num_wishes" class="wishlist_count">' + \
            str(num_wishes)+'</div>'
        print(data)
        return JsonResponse(data)
    return redirect('cart')


@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def increase_quantity(request, pk):
    if request.method == 'GET':
        cart_id = request.GET['cartid']
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.quantity_carted += 1
        cart.save()
        data = {}
        data['quantity_carted'] = '<p id="quantity_carted">'+str(cart.quantity_carted)+'</p>'
        return JsonResponse(data)
    return redirect('cart')


@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def decrease_quantity(request, pk):
    if request.method == 'GET':
        cart_id = request.GET['cartid']
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.quantity_carted -= 1
        cart.save()
        data = {}
        data['quantity_carted'] = '<p id="quantity_carted">' + \
            str(cart.quantity_carted)+'</p>'
        return JsonResponse(data)
    return redirect('cart')
