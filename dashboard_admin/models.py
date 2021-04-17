from django.db import models
from django import forms
from django.contrib.auth.models import User    #the User object is pretty much set by django.contrib.auth
# Create your models here.


class Customer(models.Model):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=50,null=True)
    mobile = models.CharField(max_length=20,null=False)
    
    def __str__(self):
        return self.name


class Seller(models.Model):
    name=models.CharField(max_length=40)
    #password = forms.CharField(widget=forms.PasswordInput)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    description = models.TextField()
    email = models.CharField(max_length=50,null=True)
    genre = models.CharField(max_length=50)
    
    #nbElementProd = models.PositiveIntegerField()
    

    def __str__(self):
        return self.name




class Product(models.Model):
    Seller=models.ForeignKey('Seller', on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
