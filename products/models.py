from django.db.models import Model, CharField, FloatField, TextField, CASCADE, ForeignKey
from django.db.models.fields.files import ImageField


class SuperCategory(Model):
    supercategory = CharField(max_length=50)

    def __str__(self):
        return self.supercategory


class Category(Model):
    supercategory = ForeignKey(
        SuperCategory, related_name='categories', on_delete=CASCADE)
    category = CharField(max_length=50)

    def __str__(self):
        return self.category


class Product(Model):
    name = CharField(max_length=100)
    supercategory = ForeignKey(
        SuperCategory, related_name='supercategories', on_delete=CASCADE)
    category = ForeignKey(
        Category, related_name='dcategories', on_delete=CASCADE)
    description = TextField()
    photo = ImageField()
    price = FloatField(default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)


# class Checkout(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     address1 = models.CharField(max_length=100)
#     address2 = models.CharField(max_length=100)
