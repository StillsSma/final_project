from django.db import models
from django.dispatch import receiver
from django.db.models import Sum

from django.db.models.signals import post_save



class InventoryItem(models.Model):
    name = models.CharField(max_length=40, unique=True)
    price_12_oz = models.FloatField()
    price_1_lbs = models.FloatField()
    price_5_lbs = models.FloatField()

    def __str__(self):
        return str(self.name)

class Invoice(models.Model):

    time_created = models.DateTimeField(auto_now_add=True)
    roaster = models.BooleanField(default=False)
    production = models.BooleanField(default=False)
    shipping = models.BooleanField(default=False)

    def order_items(self):
        return OrderItem.objects.filter(invoice=self)

    @property
    def total_cost(self):
        items = OrderItem.objects.filter(invoice=self)
        items_total = sum([order_item.total_cost for order_item in items])
        return items_total




class OrderItem(models.Model):

    GRIND = [
    ("whole bean", "WB" ),
    ("fine", "#3"),
    ("standard", "#7"),
    ("coarse", "#10")

    ]

    SIZE = [

    ("12oz","12oz"),
    ("1lbs", "1lbs"),
    ("5lbs", "5lbs")

    ]

    invoice = models.ForeignKey(Invoice)
    item = models.ForeignKey(InventoryItem)
    quantity = models.PositiveIntegerField()
    amount = models.CharField(max_length=20, choices=SIZE)
    grind = models.CharField(max_length=20, choices=GRIND)

    def __str__(self):
        return str(self.item)

    @property
    def total_cost(self):
        if self.amount == "12oz":
            return int(self.quantity) * int(self.item.price_12_oz)
        elif self.amount == "1lbs":
            return int(self.quantity) * int(self.item.price_1_lbs)
        elif self.amount == "5lbs":
            return int(self.quantity) * int(self.item.price_5_lbs)

class Customer(models.Model):

    given_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=12)
    note = models.TextField()

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
