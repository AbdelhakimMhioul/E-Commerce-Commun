import e_commerce
from django.contrib import admin
from django.urls import path, include
from products.views import SuccessView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("e_commerce.urls")),
    path('', include("users.urls")),
    path('', include("products.urls")),
]
