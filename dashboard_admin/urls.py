from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('admin_dashboard/', admin_dashboard_view, name='dashboard_admin'),
    path('view_customer/', view_customer_view, name='view_customer'),
    path('delete_customer/<int:pk>', delete_customer_view, name='delete_customer'),
    path('update_customer/<int:pk>', update_customer_view, name='update_customer'),
    path('admin_products/', admin_products_view, name='admin_products'),

    path('admin_add_product/', admin_add_product_view, name='admin_add_product'),
    path('delete_product/<int:pk>', delete_product_view, name='delete_product'),
    path('update_product/<int:pk>', update_product_view, name='update_product'),
    path('admin_view_booking/', admin_view_booking_view, name='admin_view_booking'),
    path('delete_order/<int:pk>', delete_order_view, name='delete_order'),
    path('update_order/<int:pk>', update_order_view, name='update_order'),

    path('admin_sellers/', admin_sellers_view, name='admin_sellers'),
    path('admin_add_seller', admin_add_seller_view, name='admin_add_seller'),
    path('delete_seller/<int:pk>', delete_seller_view, name='delete_seller'),
    path('update_seller/<int:pk>', update_seller_view, name='update_seller'),
    path('view_feedback', view_feedback_view, name='view_feedback'),
]
