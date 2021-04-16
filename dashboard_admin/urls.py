from django.contrib import admin
from django.urls import path
from dashboard_admin import views

urlpatterns = [
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-products', views.admin_products_view,name='admin-products'),
    
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),
    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),

    path('admin-Sellers', views.admin_Sellers_view,name='admin-Sellers'),
    path('admin-add-Seller', views.admin_add_Seller_view,name='admin-add-Seller'),
    path('delete-Seller/<int:pk>', views.delete_Seller_view,name='delete-Seller'),
    path('update-Seller/<int:pk>', views.update_Seller_view,name='update-Seller'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),
    

]