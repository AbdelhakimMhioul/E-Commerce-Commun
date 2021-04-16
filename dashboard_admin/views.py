from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings

# Create your views here.

#@login_required(login_url='login')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()
    Sellercount=models.Seller.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'Sellercount':Sellercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'dashboard_admin/admin_dashboard.html',context=mydict)


# admin view customer table
#@login_required(login_url='login')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'dashboard_admin/view_customer.html',{'customers':customers})

# admin delete customer
#@login_required(login_url='login')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    #user=models.User.objects.get(id=customer.user_id)
    #user.delete()
    customer.delete()
    return redirect('view-customer')


#@login_required(login_url='login')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    customerForm=forms.CustomerForm(instance=customer)
    
    if request.method=='POST':
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if  customerForm.is_valid():
            customerForm.save()
            return redirect('view-customer')
    return render(request,'dashboard_admin/admin_update_customer.html',{'customerForm':customerForm})






# admin view the product
#@login_required(login_url='login')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'dashboard_admin/admin_products.html',{'products':products})


# admin add product by clicking on floating button
#@login_required(login_url='login')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'dashboard_admin/admin_add_products.html',{'productForm':productForm})


#@login_required(login_url='login')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


#@login_required(login_url='login')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'dashboard_admin/admin_update_product.html',{'productForm':productForm})


#@login_required(login_url='login')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'dashboard_admin/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


#@login_required(login_url='login')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
#@login_required(login_url='login')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'dashboard_admin/update_order.html',{'orderForm':orderForm})


# admin view the feedback
#@login_required(login_url='login')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'dashboard_admin/view_feedback.html',{'feedbacks':feedbacks})






# admin view the Seller
#@login_required(login_url='login')
def admin_Sellers_view(request):
    Sellers=models.Seller.objects.all()
    return render(request,'dashboard_admin/admin_Sellers.html',{'Sellers':Sellers})


# admin add Seller by clicking on floating button
#@login_required(login_url='login')
def admin_add_Seller_view(request):
    SellerForm=forms.SellerForm()
    if request.method=='POST':
        SellerForm=forms.SellerForm(request.POST, request.FILES)
        if SellerForm.is_valid():
            SellerForm.save()
        return HttpResponseRedirect('admin-Sellers')
    return render(request,'dashboard_admin/admin_add_Sellers.html',{'SellerForm':SellerForm})


#@login_required(login_url='login')
def delete_Seller_view(request,pk):
    Seller=models.Product.objects.get(id=pk)
    Seller.delete()
    return redirect('admin-Sellers')


#@login_required(login_url='login')
def update_Seller_view(request,pk):
    Seller=models.Seller.objects.get(id=pk)
    SellerForm=forms.SellerForm(instance=Seller)
    if request.method=='POST':
        SellerForm=forms.SellerForm(request.POST,request.FILES,instance=Seller)
        if SellerForm.is_valid():
            SellerForm.save()
            return redirect('admin-Sellers')
    return render(request,'dashboard_admin/admin_update_Seller.html',{'SellerForm':SellerForm})

