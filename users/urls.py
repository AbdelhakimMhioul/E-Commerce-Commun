from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('dashboardClient/', showDashbordClient, name='dashboardclient'),
    path('dashboardSeller/', showDashbordSeller, name='dashboardseller'),
    path('myAccount', myAccount, name='myAccount'),
]
