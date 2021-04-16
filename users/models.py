from django.db import models

# Create your models here.

USERS = (
    ('SELLER', 'SELLER'),
    ('CLIENT', 'CLIENT'),
)


class Choice(models.Model):
    choice = models.CharField(max_length=100, choices=USERS)
