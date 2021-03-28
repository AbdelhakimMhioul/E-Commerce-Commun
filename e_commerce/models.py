from django.db import models
from django.db.models.fields import EmailField
from django.db.models.fields.files import ImageField
from phone_field import PhoneField

# Create your models here.


class Seller(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    photo = ImageField()
    genre = models.CharField(max_length=50)
    email = EmailField(max_length=254)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    nbElementProd = models.PositiveBigIntegerField()
    resteProd = models.PositiveBigIntegerField()
    profitProd = models.FloatField()

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.name
