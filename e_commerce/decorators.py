from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'SELLER':
            return redirect('dashboardseller')
        if group == 'CLIENT':
            return redirect('home')
        if group == 'ADMIN':
            return view_func(request, *args, **kwargs)
    return wrapper_func


def client_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'SELLER':
            return redirect('dashboardseller')
        if group == 'CLIENT':
            return view_func(request, *args, **kwargs)
        if group == 'ADMIN':
            return view_func(request, *args, **kwargs)
    return wrapper_func


def seller_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'SELLER':
            return view_func(request, *args, **kwargs)
        if group == 'CLIENT':
            return redirect('home')
        if group == 'ADMIN':
            return view_func(request, *args, **kwargs)
    return wrapper_func


