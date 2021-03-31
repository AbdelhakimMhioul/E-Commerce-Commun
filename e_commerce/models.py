from django.db.models import Model, CharField, FloatField, TextField, CASCADE, ForeignKey, PositiveBigIntegerField
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


class Category(Model):
    category = CharField(max_length=50)

    def __str__(self):
        return self.category


class Product(Model):
    name = CharField(max_length=100)
    category = ForeignKey(
        Category, related_name='dcategories', on_delete=CASCADE)
    description = TextField()
    photo = ImageField()
    price = FloatField(default=0)

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
