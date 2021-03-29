from django.db.models import Model, TextField, CharField, PositiveBigIntegerField, FloatField
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
