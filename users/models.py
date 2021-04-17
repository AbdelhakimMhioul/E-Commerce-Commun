from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'


class Seller(models.Model):
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    phone = models.CharField(max_length=190, null=True)
    age = models.CharField(max_length=190, null=True)
    avatar = models.ImageField(blank=True, null=True, default="preson.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
