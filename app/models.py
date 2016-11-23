from django.db import models
from django.dispatch import receiver

from django.db.models.signals import post_save



class InventoryItem(models.Model):
    name = models.CharField(max_length=40, unique=True)
    price_per_oz = models.FloatField()

    def __str__(self):
        return str(self.name)

class Invoice(models.Model):

    time_created = models.DateTimeField(auto_now_add=True)
    roaster = models.BooleanField(default=False)
    production = models.BooleanField(default=False)
    shipping = models.BooleanField(default=False)

    def order_items(self):
        return OrderItem.objects.filter(invoice=self)



class OrderItem(models.Model):

    GRIND = [
    ("whole bean", "WB" ),
    ("fine", "#3"),
    ("standard", "#7"),
    ("coarse", "#10")

    ]

    SIZE = [
    ("8", "8oz"),
    ("9", "9oz"),
    ("10", "10oz"),
    ("11","11oz"),
    ("12","12oz"),
    ("16", "1lbs"),
    ("80", "5lbs")

    ]

    invoice = models.ForeignKey(Invoice)
    item = models.ForeignKey(InventoryItem)
    quantity = models.PositiveIntegerField()
    amount = models.CharField(max_length=20, choices=SIZE)
    grind = models.CharField(max_length=20, choices=GRIND)

    def __str__(self):
        return str(self.item)

class Profile(models.Model):
    ACCESS_LEVELS = [
    ("c", "Customer Service"),
    ("r", "Roasting"),
    ("o", "Production"),
    ("d", "Delivery")
    ]

    user = models.OneToOneField('auth.User')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS)

    @receiver(post_save, sender='auth.user')
    def create_profile(sender, **kwargs):
        instance = kwargs["instance"]
        created = kwargs["created"]
        if created:
            Profile.objects.create(user=instance)
