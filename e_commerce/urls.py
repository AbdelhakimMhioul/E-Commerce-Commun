from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('checkout/', checkout, name='checkout'),
    path('cart', cart, name="cart"),
    path('view-product/<int:pk>', viewProduct, name="viewProduct"),
    path('view-product/<int:pk>', rated, name="rated"),
    path('categorie/<str:categorie>', categorie, name="categorie")
]
