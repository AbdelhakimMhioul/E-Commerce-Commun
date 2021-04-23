from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from ..models import *
from ..forms import CheckoutForm
from django.contrib.auth.models import Group

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
                if form.is_valid():
                    adress1 = form.cleaned_data.get('adress_1')
                    adress2 = form.cleaned_data.get('adress_2')
                    zipcode = form.cleaned_data.get('zip_code')
                    countryy = form.cleaned_data.get('country') 
                    checkoutadress = Checkout.objects.create(
                        user = request.user,
                        adress_1 = adress1,
                        adress_2 = adress2,
                        zip_code = zipcode,
                        country = countryy
                    )
                    order = Order.objects.create(user= request.user, checkout_adress= checkoutadress,status= 'Payed')
                    order.save()
                    for product in carts:
                        order.cart.add(product)
                    
                    products= order.cart.all() # queryset :all products in  cart.
                    for product in products:
                        print(product)
                    print("reussi")
                    return redirect('home')
            except:
                print("n'est pas reussi")
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
