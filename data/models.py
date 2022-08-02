from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=1020)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
