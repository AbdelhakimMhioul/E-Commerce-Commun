from .models import Category, Product
from django.shortcuts import render, redirect
from .forms import CheckoutForm

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, }
    return render(request, 'home.html', context)


def checkout(request):
    formCheckout = CheckoutForm()
    if request.method == 'POST':
        formCheckout = CheckoutForm(request.POST)
        if formCheckout.is_valid():
            formCheckout.save()
            return redirect('home')

    context = {'formCheckout': formCheckout}
    return render(request, 'checkout.html', context)


def cart(request):
    return render(request, 'cart.html', {})


def viewProduct(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    print(product)
    return render(request, 'viewProduct.html', context)
