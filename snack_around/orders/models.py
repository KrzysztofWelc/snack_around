from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    restaurant = models.ForeignKey(get_user_model(), related_name='products', on_delete=models.CASCADE)


class Order(models.Model):
    ordered_by = models.ForeignKey(get_user_model(), related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=450)
    phone_num = models.CharField(max_length=25)
