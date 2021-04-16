from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category',
              'description', 'photo', 'price', 'quantity']


admin.site.register(Product, ProductAdmin)
admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Seller)
