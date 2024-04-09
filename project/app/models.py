from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    fio = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fio']


class Products(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    price = models.IntegerField()


class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Orders(models.Model):
    products = models.ManyToManyField(Products)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_price = models.IntegerField()