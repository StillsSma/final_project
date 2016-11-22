from django.db import models
from django.dispatch import receiver

from django.db.models.signals import post_save



class InventoryItem(models.Model):
    name = models.CharField(max_length=40, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()

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

    invoice = models.ForeignKey(Invoice)
    item = models.CharField(max_length=50)
    quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    grind = models.CharField(max_length=20, choices=GRIND)

    def __str__(self):
        return self.item

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
