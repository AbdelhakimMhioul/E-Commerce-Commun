from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from main.models import Product
from main.forms import CreateProductForm
from main.filters import ProductFilter
from accounts.decorators import allowed_users
from main.models import WishlistProduct, Cart


def show_dashboard(request):
    return render(request, 'dashboard_seller/home.html')


def show_statistics(request):
    return render(request, 'dashboard_seller/statistics.html')


def show_map(request):
    return render(request, 'dashboard_seller/map.html')


def show_calendar(request):
    return render(request, 'dashboard_seller/cc.html')


def show_settings(request):
    return render(request, 'dashboard_seller/settings/base.html')


def show_general(request):
    return render(request, 'dashboard_seller/settings/general.html')


def show_change_password(request):
    return render(request, 'dashboard_seller/settings/changePassword.html')


def show_product(request):
    form = CreateProductForm()
    products = Product.objects.all()
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            print("printing", request.POST)
            form.save()
            return redirect('/prod')
        else:
            print("ERROR HADXI MAKHADAMX")
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'form': form, 'products': products,
               'myFilter': myFilter,
               }
    return render(request, 'dashboard_seller/products.html', context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('prod')
    context = {'item': product}
    return render(request, 'dashboard_seller/delete_product.html', context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = CreateProductForm(instance=product)
    if request.method == 'POST':
        form = CreateProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('prod')
    context = {'form': form}
    return render(request, 'dashboard_seller/products.html', context)


def result_data(request):
    date_data = []
    products = Product.objects.all()
    for i in products:
        date_data.append({i.name: i.quantity})
    print(dateData)
    return JsonResponse(dateData, safe=False)


# @login_required
# @allowed_users(allowed_roles=['ADMIN', 'SELLER'])
# def dashboard_seller(request):
#     num_wishes = WishlistProduct.objects.count()
#     num_carts = Cart.objects.count()
#     total_price = 0
#     carts = Cart.objects.all()
#     for order in carts:
#         total_price += order.order_total_price()
#     context = {'num_carts': num_carts, 'num_wishes': num_wishes,
#                'total_price': total_price}
#     return render(request, 'accounts/dashboard_seller.html', context)
