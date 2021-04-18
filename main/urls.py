from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('checkout/', checkout, name='checkout'),
    path('view_product/<int:pk>/', view_product, name="view_product"),
    path('rated/<int:pk>/', rated, name="rated"),
    path('unrated/<int:pk>/', unrated, name="unrated"),
    path('categorie/<int:pk>', categorie, name="categorie"),
    path('wishlist/', wishlist, name="wishlist"),
    path('add_wishlist/<int:pk>', add_wishlist, name="add_wishlist"),
    path('eliminate_wish/<int:pk>', eliminate_wish, name="eliminate_wish"),
    path('add_cart/<int:pk>', add_cart, name="add_cart"),
    path('delete_cart/<int:pk>', delete_cart, name="delete_cart"),
    path('cart/', cart, name="cart"),
    path('increase_quantity/<int:pk>',increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:pk>',
         decrease_quantity, name='decrease_quantity'),
    path('search_form/', search_form, name="search_form"),
]