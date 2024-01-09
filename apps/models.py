from django.db import models


# Create your models here.
class Timestamp(models.Model):
    """
    Timestamp mixin to inherit
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # prevent dj from creating a column for this table
    class Meta:
        abstract = True
