from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for'+user)
            return redirect('login')

    context={'form':form}
    return render(request,'users/register.html',context)
def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not  None:
            login(request,user)
            return redirect('register')
        else:
            messages.info(request,'Username or passwordin incorrect')
            return render(request,'users/login.html')
    return render(request,'users/login.html')
 
