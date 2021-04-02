from django.urls import path
from . import views


urlpatterns = [
    path('dashboardSeller/', views.showDashboard, name='dashboardSeller'),
    path('prod/', views.showProduct, name='prod'),
    path('statistics/', views.showStatistics, name='statistics'),
    path('settings/', views.showSettings, name='settings'),
    path('resultsData/', views.ResultData, name='result'),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),
]
