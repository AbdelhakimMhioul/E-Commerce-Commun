from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login as auth_login,authenticate
from django.contrib import messages 


def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('register.html')
        else:
            messages.info(request, 'Username or Password incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')

