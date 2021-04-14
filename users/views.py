from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm
from e_commerce.models import WishlistProduct, Order
from django.contrib.auth.decorators import login_required


def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if form.cleaned_data['choice'] == 'CLIENT':  
                return redirect('home')
            if form.cleaned_data['choice'] == 'SELLER':
                return redirect('prod')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


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


@login_required
def viewAccount(request):
    numWishes = WishlistProduct.objects.count()
    numOrder = Order.objects.count()
    total_price = 0
    orders = Order.objects.all()
    for order in orders:
        total_price += order.order_total_price()
    context = {'user': request.user, 'numOrder': numOrder,
               'numWishes': numWishes, 'total_price': total_price}
    return render(request, 'accounts/myAccount.html', context)


@login_required
def editAccount(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account/profile/')
    return render(request, 'accounts/myAccount.html')


@login_required
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset/password_reset.html", context={"password_reset_form": password_reset_form})


@login_required
def showDashboardClient(request):
    numWishes = WishlistProduct.objects.count()
    numOrder = Order.objects.count()
    total_price = 0
    orders = Order.objects.all()
    for order in orders:
        total_price += order.order_total_price()
    context = {'numOrder': numOrder, 'numWishes': numWishes,
               'total_price': total_price}
    return render(request, 'accounts/dashboardClient.html', context)


@login_required
def showDashboardSeller(request):
    numWishes = WishlistProduct.objects.count()
    numOrder = Order.objects.count()
    total_price = 0
    orders = Order.objects.all()
    for order in orders:
        total_price += order.order_total_price()
    context = {'numOrder': numOrder, 'numWishes': numWishes,
               'total_price': total_price}
    return render(request, 'accounts/dashboardSeller.html', context)
