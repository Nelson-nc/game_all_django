import random
import time

from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = ('pending', 'pending')
        DELIVERD = ('deliverd', 'deliverd')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    total_amount = models.DecimalField(decimal_places=2, max_digits=8, default=0.00) # type: ignore
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order for {self.user.username} on {self.created_on}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0.00) # type: ignore

    def get_price(self) -> None:
        price: float = float(self.product.price) * float(self.quantity)
        self.price = price
