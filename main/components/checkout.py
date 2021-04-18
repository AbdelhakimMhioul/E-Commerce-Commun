from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from ..models import *


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
