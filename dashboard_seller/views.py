from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from main.models import Product
from main.forms import CreateProductForm
from main.filters import ProductFilter
from accounts.decorators import allowed_users
from main.models import WishlistProduct, Cart,OrderItem
from accounts.forms import CreateUserForm
from django.contrib.auth.models import User

@allowed_users(allowed_roles=['SELLER'])
@login_required
def show_dashboard(request):
    products = Product.objects.filter(user=request.user)
    nb_products=products.count()
 
    orders =  OrderItem.objects.filter(user=request.user)
    products_ordered= 0
    paid_amount = 0
    total_order=0
    for item in orders:

        products_ordered+= item.quantity
        paid_amount+=item.price *item.quantity

        

    context={'nb_products':nb_products,
    'products_ordered':products_ordered,
    ' paid_amount': paid_amount,
    'total_order':total_order,}
    return render(request, 'dashboard_seller/home.html',context)


@login_required
def show_statistics(request):
    return render(request, 'dashboard_seller/statistics.html')

@login_required
def show_map(request):
    return render(request, 'dashboard_seller/map.html')

@login_required
def show_calendar(request):
    return render(request, 'dashboard_seller/cc.html')

@login_required
def show_settings(request):
    return render(request, 'dashboard_seller/settings/base.html')


def show_general(request):
    userform = User.objects.get(id=request.user.id)
    form = CreateUserForm(instance=userform)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=userform)
        if form.is_valid():
            form.save()
            return redirect('general')
    context = {'form': form}
    return render(request, 'dashboard_seller/settings/general.html',context)


def show_change_password(request):
    return render(request, 'dashboard_seller/settings/changePassword.html')

@allowed_users(allowed_roles=['SELLER'])
@login_required
def show_product(request):
    form = CreateProductForm()
    products = Product.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.user=request.user
            product.save()
            return redirect('prod')
        else:
            print("ERROR HADXI MAKHADAMX")
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'form': form, 'products': products,
               'myFilter': myFilter,
               }
    return render(request, 'dashboard_seller/products.html', context)

@login_required
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('prod')
    context = {'item': product}
    return render(request, 'dashboard_seller/delete_product.html', context)

@login_required
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

@login_required
def result_data(request):
    date_data = []
    products = Product.objects.filter(user=request.user)
    for i in products:
        date_data.append({i.name: i.quantity})
    print(dateData)
    return JsonResponse(dateData, safe=False)
