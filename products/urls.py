from django.urls import path
from products import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('dashbordclient/', views.showDashbord, name='dashbordclient'),
    path('cart', views.cart, name="cart"),
]
