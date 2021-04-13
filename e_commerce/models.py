from django.db.models import Model, CharField, FloatField, TextField, CASCADE, ForeignKey, IntegerField, SET_NULL
from django.db.models.fields.related import OneToOneField
from django.forms import ChoiceField, RadioSelect
from django.db.models.fields import EmailField, PositiveIntegerField
from django.db.models.fields.files import ImageField
from phone_field import PhoneField
from django.contrib.auth.models import User

# Create your models here.

TRADE_ROLE = (
    (0, 'SELLER'),
    (1, 'CLIENT'),
    (2, 'BOTH'),
)


class Category(Model):
    category = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category


class Product(Model):
    name = CharField(max_length=100)
    category = ForeignKey(
        Category, related_name='categories', on_delete=CASCADE)
    description = TextField()
    photo = ImageField()
    price = FloatField(default=0)
    quantity = PositiveIntegerField(null=True)
    good_rates = PositiveIntegerField(default=0)
    bad_rates = PositiveIntegerField(default=0)
    rates = PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)

    def avg_rate(self):
        self.rates = (self.good_rates-self.bad_rates)/(self.bad_rates +
                                                       self.good_rates) if self.bad_rates+self.good_rates != 0 else 0
        return self.rates


class Person(Model):
    name = CharField(max_length=50)
    photo = ImageField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = EmailField(max_length=254)
    trade = ChoiceField(choices=TRADE_ROLE, widget=RadioSelect)

    def __str__(self):
        return self.name


class Seller(Person):
    description = TextField()
    genre = CharField(max_length=50)
    nbElementProd = PositiveIntegerField()
    resteProd = PositiveIntegerField()
    profitProd = FloatField()

    def __str__(self):
        return super().name


class WishlistProduct(Model):
    user = ForeignKey(
        User, related_name='wishlist', on_delete=CASCADE)
    product = OneToOneField(Product, on_delete=CASCADE, unique=True)

    def __str__(self):
        return self.product.name


class Cart(Model):
    user = ForeignKey(User, related_name='cart', on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)

    def __str__(self):
        return self.product.name


class Customer(Model):
    user = OneToOneField(
        User, on_delete=CASCADE, null=True, blank=True)
    name = CharField(max_length=50)
    photo = ImageField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = EmailField(max_length=254)
    trade = ChoiceField(choices=TRADE_ROLE, widget=RadioSelect)

    def __str__(self):
        return self.name


class User_Customer(Model):
    customer = ForeignKey(
        Customer, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def Total_Price(self, product_total_price):
        customerforproducts = self.customerforproduct_set.all()
        for product in customerforproducts:
            total = total+product.product_total_price
        return total


class CustomerForProduct(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    usercustomer = ForeignKey(
        User_Customer, on_delete=SET_NULL, null=True)

    def product_total_price(self):
        total = self.product.price * self.product.quantity
        return total
