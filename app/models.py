from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=40)
    price = models.FloatField()
    quantity = models.IntegerField()
    
