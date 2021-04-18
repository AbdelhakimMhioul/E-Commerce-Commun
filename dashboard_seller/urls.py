from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('dashboard_seller/', views.show_dashboard, name='dashboard_seller'),
    path('prod/', views.show_product, name='prod'),
    path('statistics/', views.show_statistics, name='statistics'),
    path('settings/', views.show_settings, name='settings'),
    path('map/', views.show_map, name='map'),
    path('calendar/', views.show_calendar, name='calendar'),
    path('settings/general', views.show_general, name='general'),
    path('results_data/', views.result_data, name='result'),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),
    path('settings/change-password/', auth_views.PasswordChangeView.as_view(
         template_name='dashboard_seller/settings/change_password.html'), name="change_password"),
]
