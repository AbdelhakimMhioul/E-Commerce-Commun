from django.db import models
from django.db.models.fields.related import OneToOneField
from django.forms import ChoiceField, RadioSelect
from django.db.models.fields import EmailField, PositiveIntegerField
from django.db.models.fields.files import ImageField
from phone_field import PhoneField
from django.contrib.auth.models import User
from users.models import Client, Seller

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


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField()
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(null=True)
    good_rates = models.PositiveIntegerField(default=0)
    bad_rates = models.PositiveIntegerField(default=0)
    rates = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)

    def avg_rate(self):
        self.rates = (self.good_rates-self.bad_rates)/(self.bad_rates +
                                                       self.good_rates) if self.bad_rates+self.good_rates != 0 else 0
        return self.rates


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
    client = models.ForeignKey(
        Client, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        Product(), null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)


# class Checkout(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, null=True, blank=True)
#     address_1 = models.CharField(max_length=100)
#     address_2 = models.CharField(max_length=100, blank=True)
#     city = models.CharField(max_length=100)
#     state = ChoiceField(choices=STATES)
#     zip_code = models.CharField(max_length=100)
#     check_me_out = models.BooleanField()
