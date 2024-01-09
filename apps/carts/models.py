from django.db import models
from ..models import Timestamp
from ..products.models import Products
import uuid
from django.contrib.auth.models import User


# Create your models here.
PRODUCT_STATUS = [
    ("processing", "Processing"),
    ("pending", "Pending"),
    ("in transit", "In Transit"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
    ("rejected", "Rejected")
]

class UserCart(Timestamp):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    cart_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default="pending", choices=PRODUCT_STATUS)
    active = models.BooleanField(default=True)
