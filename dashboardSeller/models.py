from django.db import models
from django.db.models.fields.files import ImageField

# Create your models here.

class Productt(models.Model):
    CATEGORY = (
			('Accessoirs', 'Accessoirs'),
			('Sacs', 'Sacs'),
            ('Chaussures', 'Chaussures'),
            ('Robes', 'Robes'),
			) 
    name=models.CharField(max_length=100)
    description = models.TextField()
    photo = ImageField()
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    price = models.FloatField(null=True)
    quantity=models.IntegerField(null=True)

    def __str__(self):
        return self.name