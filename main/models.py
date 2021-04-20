from django.db import models
from django.db.models.fields.related import OneToOneField
from django.forms import ChoiceField, RadioSelect
from django.db.models.fields import EmailField, PositiveIntegerField
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import Group
from phone_field import PhoneField

from django import forms
# the User object is pretty much set by django.contrib.auth
from django.contrib.auth.models import User
# Create your models here

TRADE_ROLE = (
    (0, 'SELLER'),
    (1, 'CLIENT'),
    (2, 'BOTH'),
)

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

COLORS = (
    ('RED', 'RED'),
    ('BLUE', 'BLUE'),
    ('BLACK', 'BLACK'),
)
category=(
    ('Vetement','Vetement'),
)

class Category(models.Model):
  
    category=models.CharField(max_length=200,null=True,choices=category)
    def __str__(self):
        return self.category


class Product(models.Model):
    user=models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    category=models.CharField(max_length=200,null=True,choices=category)
    description = models.TextField()
    photo = models.ImageField(blank=True,)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(null=True)
    good_rates = models.PositiveIntegerField(default=0)
    bad_rates = models.PositiveIntegerField(default=0)
    rates = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50, choices=COLORS, blank=True)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)

    def avg_rate(self):
        self.rates = (self.good_rates-self.bad_rates)/(self.bad_rates +
                                                       self.good_rates) if self.bad_rates+self.good_rates != 0 else 0
        return self.rates


class ProductsRated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE)
    rated = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class WishlistProduct(models.Model):
    user = models.ForeignKey(
        User, related_name='wishlist', on_delete=models.CASCADE)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_carted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name

    def cart_total_price(self):
        total_cart = self.quantity_carted*self.product.price
        return total_cart


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('in progress', 'in progress'),
        ('out of order', 'out of order')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
   

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return '%s' % self.id

class Checkout(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    adress_1 = models.CharField(max_length=100)
    adress_2 = models.CharField(max_length=100, blank=True)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    check_me_out = models.BooleanField()

class ProductsFeedBacks(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=False)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name


