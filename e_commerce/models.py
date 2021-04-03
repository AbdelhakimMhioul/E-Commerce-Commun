from django.db.models import Model, CharField, FloatField, TextField, CASCADE, ForeignKey, PositiveBigIntegerField, IntegerField
from django.db.models.fields.related import OneToOneField
from django.forms import ChoiceField, RadioSelect
from django.db.models.fields import EmailField
from django.db.models.fields.files import ImageField
from phone_field import PhoneField

# Create your models here.

TRADE_ROLE = (
    (0, 'SELLER'),
    (1, 'CLIENT'),
    (2, 'BOTH'),
)

INTEGERS = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Category(Model):
    category = CharField(max_length=50)

    def __str__(self):
        return self.category


class Product(Model):
    name = CharField(max_length=100)
    category = ForeignKey(
        Category, related_name='categories', on_delete=CASCADE)
    description = TextField()
    photo = ImageField()
    price = FloatField(default=0)
    quantity = PositiveBigIntegerField(null=True)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)


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
    nbElementProd = PositiveBigIntegerField()
    resteProd = PositiveBigIntegerField()
    profitProd = FloatField()

    def __str__(self):
        return super().name


class Rating(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    rates = IntegerField(choices=INTEGERS, default=0)

    def increment_rate(self):
        self.rates += 1

    def decrement_rate(self):
        self.rates -= 1

    def __str__(self):
        return self.product.name


class WishlistProduct(Model):
    product = OneToOneField(Product, on_delete=CASCADE,unique=True)

    def __str__(self):
        return self.product.name


# class Checkout(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     address1 = models.CharField(max_length=100)
#     address2 = models.CharField(max_length=100)
