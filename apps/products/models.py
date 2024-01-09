from django.db import models
from ..models import Timestamp
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField


# Create your models here.

def short_uuid():
    return str(uuid.uuid4())[:8]


class Categories(Timestamp):
    category_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    category_image = CloudinaryField("image", null=True,blank=True,default=None)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category_name}"
    
    @property
    def category_image_url(self):
        return self.category_image.url if self.category_image else None

class Products(Timestamp):
    product_id = models.CharField(primary_key=True, default=short_uuid, editable=False, db_index=True, unique=True, max_length=8)
    product_name = models.CharField(max_length=250)
    product_image = CloudinaryField("image", null=True,blank=True,default=None)
    brand = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    size = models.IntegerField(default=0, blank=True)
    discount = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    exp_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.product_name}"
    
    @property
    def product_image_url(self):
        return self.product_image.url if self.product_image else None
    
class Scans(Timestamp):
    scan_id = models.CharField(primary_key=True, default=short_uuid, editable=False, db_index=True, unique=True, max_length=8)
    scan_image = models.ImageField(upload_to="scanned/")

    def delete(self, *args, **kwargs):
        # Delete the media file from storage before deleting the model instance
        storage, path = self.scan_image.storage, self.scan_image.path
        super().delete(*args, **kwargs)
        storage.delete(path)

