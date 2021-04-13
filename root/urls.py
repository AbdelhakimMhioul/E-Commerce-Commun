from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("e_commerce.urls")),
    path('', include("users.urls")),
    path('', include("api.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
