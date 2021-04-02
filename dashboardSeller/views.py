from django.shortcuts import render, redirect
from e_commerce.models import Product
from .forms import CreateProductForm
from .filters import ProductFilter
from django.http import JsonResponse


def showDashboard(request):
    return render(request, 'dashboardSeller/home.html')


def showStatistics(request):
    return render(request, 'dashboardSeller/statistics.html')


def showSettings(request):
    return render(request, 'dashboardSeller/settings.html')


def showProduct(request):
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
<<<<<<< HEAD
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'form': form, 'products': products,
               'myFilter': myFilter,
               }
    return render(request, 'dashboardSeller/products.html', context)


def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
=======
    myFilter=ProductFilter(request.GET,queryset=products)
    products=myFilter.qs
    context={'form':form,
             'products':products,
             'myFilter':myFilter,
             }
    return render(request,'dashBoardSeller/products.html',context)

def deleteProduct(request, pk):
	product = Productt.objects.get(id=pk)
>>>>>>> b140bbb5122c119a246cb3c5ebb4ce76d39d2ecd
	if request.method == "POST":
		product.delete()
		return redirect('/prod')

<<<<<<< HEAD
	context = {'item': product}
	return render(request, 'dashboardSeller/products.html', context)


def updateProduct(request, pk):

	product = Product.objects.get(id=pk)
	form = CreateProductForm(instance=product)

	if request.method == 'POST':
		form = CreateProductForm(request.POST, instance=product)
=======
	context = {'item':product}
	return render(request, 'dashBoardSeller/products.html', context)

def updateProduct(request, pk):

	product = Productt.objects.get(id=pk)
	form = FormProduct(instance=product)

	if request.method == 'POST':
		form = FormProduct(request.POST, instance=product)
>>>>>>> b140bbb5122c119a246cb3c5ebb4ce76d39d2ecd
		if form.is_valid():
			form.save()
			return redirect('/prod')

<<<<<<< HEAD
	context = {'form': form}
	return render(request, 'dashboardSeller/products.html', context)


def ResultData(request):
    dateData = []
    products = Product.objects.all()
    for i in products:
        dateData.append({i.name: i.quantity})
    print(dateData)
    return JsonResponse(dateData, safe=False)
=======
	context = {'form':form}
	return render(request, 'dashBoardSeller/products.html', context)

def ResultData(request):
    dateData=[]
    products=products=Productt.objects.all()
    
    for i in products:
        dateData.append({i.name:i.quantity})
    print(dateData)
    return JsonResponse(dateData,safe=False)
>>>>>>> b140bbb5122c119a246cb3c5ebb4ce76d39d2ecd
