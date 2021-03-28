from django.db import models
from django.db.models.fields.files import ImageField

class Product(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField()
    photo = ImageField()
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)
