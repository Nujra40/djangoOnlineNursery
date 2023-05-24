from django.db import models

# Create your models here.

class Details(models.Model):
    Name = models.CharField(max_length=20, default="")
    Scientific_Name = models.CharField(max_length=20, default="")
    Price = models.IntegerField(max_length=6, default="")
    Properties = models.TextField(default="")
    Img_path = models.TextField(default="")
    Initial_quantity = models.IntegerField(max_length=5, default=1)
    Quantity = models.IntegerField(max_length=5, default=1)
    Add_to_cart = models.CharField(max_length=10, default="Add")
    type = models.CharField(max_length=20, default="")
