from django.contrib import admin
from .models import *

# Register your models here.


# class SellerAdmin(admin.ModelAdmin):
#     list_display = ("name", "phone",)


# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("name", "phone",)


# admin.site.register(Seller, SellerAdmin)
admin.site.register(Person)
