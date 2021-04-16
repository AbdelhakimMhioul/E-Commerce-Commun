from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin-dashboard/', admin_dashboard_view,name='admin-dashboard'),
    path('view-customer/', view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', update_customer_view,name='update-customer'),
    path('admin-products/', admin_products_view,name='admin-products'),
    
    path('admin-add-product/', admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', update_product_view,name='update-product'),
    path('admin-view-booking/', admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', update_order_view,name='update-order'),

    path('admin-sellers/', admin_Sellers_view,name='admin-Sellers'),
    path('admin-add-seller', admin_add_Seller_view,name='admin-add-Seller'),
    path('delete-seller/<int:pk>', delete_Seller_view,name='delete-Seller'),
    path('update-seller/<int:pk>', update_Seller_view,name='update-Seller'),
    path('view-feedback', view_feedback_view,name='view-feedback'),
    

]