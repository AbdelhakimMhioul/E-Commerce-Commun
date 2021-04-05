from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('checkout/', checkout, name='checkout'),
    path('view-product/<int:pk>/', viewProduct, name="viewProduct"),
    path('rated/<int:pk>/', rated, name="rated"),
    path('unrated/<int:pk>/', unrated, name="unrated"),
    path('categorie/<str:categorie>', categorie, name="categorie"),
    path('addwishlist/<int:pk>', addWishlist, name="addWishlist"),
    path('eliminateWish/<int:pk>', eliminateWish, name="eliminateWish"),
    path('wishlist/', wishlist, name="wishlist"),
    path('addCart/<int:pk>', addCart, name="addCart"),
    path('eliminateCart/<int:pk>', eliminateCart, name="eliminateCart"),
    path('cart/', cart, name="cart"),
    path('increaseQuantity/', increaseQuantity, name='increaseQuantity'),
    path('decreaseQuantity/', decreaseQuantity, name='decreaseQuantity'),
    path('search_form/', search_form, name="search_form"),
]
