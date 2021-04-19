from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from ..models import *
from ..forms import CheckoutForm


@login_required
def checkout(request):
    form = CheckoutForm()
    num_wishes = WishlistProduct.objects.count()
    num_carts = Cart.objects.count()
    total_price = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            total_price += cart.cart_total_price()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            cart = Cart.objects.get(user=request.user)
            if form.is_valid():
                adress_1 = form.cleand_data.get(' adress_1 ')
                adress_2 = form.cleand_data.get(' adress_2 ')
                zip_code = form.cleand_data.get(' zip_code ')
                country = form.cleand_data.get(' country')
                checkout_adress = Checkout(
                    user=request.user,
                    adress_1=adress_1,
                    adress_2=adress_1,
                    zip_code=zip_code,
                    country=country
                )
                checkout_adress.save()
                #cart.checkout_adress= checkout_adress
                # cart.save()
                return redirect('home')
        except:
            return redirect('home')
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    context = {'form': form, 'group': group,
               'num_carts': num_carts, 'num_wishes': num_wishes, 'total_price': total_price}
    return render(request, 'checkout.html', context)
