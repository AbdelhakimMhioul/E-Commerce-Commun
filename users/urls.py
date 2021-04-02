from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import UserForgotPasswordForm

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard_client/', showDashbordClient, name='dashboardclient'),
    path('account/profile/', viewAccount, name='viewAccount'),
    path('account/profile/edit', editAccount, name='editAccount'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html'), name="change_password"),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html'), name="change_password_done"),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset/password_reset.html', email_template_name="accounts/password_reset/password_reset_email.txt", success_url='password_reset_done', from_email='hk.mhl1975@gmail.com'), name="password_reset"),
    path('accounts/password_reset/password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset/password_reset_form.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset/password_reset_done.html"), name='password_reset_complete'),
]
