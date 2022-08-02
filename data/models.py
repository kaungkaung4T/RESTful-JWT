from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=1020)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
