from django.shortcuts import render,redirect
from .models import Productt
from .forms import FormProduct
from .filters import  ProductFilter
from django.http import JsonResponse

def showDashbord(request):
    return render(request,'dashBoardSeller/home.html')

def showStatistics(request):
    return render(request,'dashBoardSeller/statistics.html')

def showSettings(request):
    return render(request,'dashBoardSeller/settings.html')
def ShowProduct(request):
    form=FormProduct
    products=Productt.objects.all()
    if request.method== 'POST':
        form=FormProduct(request.POST)
        if form.is_valid():
            print("printing" ,request.POST)
            form.save()
            return redirect('/prod')
        else:
            print("ERROR HADXI MAKHADAMX")
    myFilter=ProductFilter(request.GET,queryset=products)
    products=myFilter.qs
    context={'form':form,
             'products':products,
             'myFilter':myFilter,
             }
    return render(request,'dashBoardSeller/products.html',context)

def deleteProduct(request, pk):
	product = Productt.objects.get(id=pk)
	if request.method == "POST":
		product.delete()
		return redirect('/prod')

	context = {'item':product}
	return render(request, 'dashBoardSeller/products.html', context)

def updateProduct(request, pk):

	product = Productt.objects.get(id=pk)
	form = FormProduct(instance=product)

	if request.method == 'POST':
		form = FormProduct(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('/prod')

	context = {'form':form}
	return render(request, 'dashBoardSeller/products.html', context)

def ResultData(request):
    dateData=[]
    products=products=Productt.objects.all()
    
    for i in products:
        dateData.append({i.name:i.quantity})
    print(dateData)
    return JsonResponse(dateData,safe=False)