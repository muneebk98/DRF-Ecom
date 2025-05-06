from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='', blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(default=1)
