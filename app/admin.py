from django.contrib import admin

# Register your models here.
from app.models import InventoryItem, Profile, Invoice, OrderItem

admin.site.register(InventoryItem)
admin.site.register(Profile)
admin.site.register(Invoice)
admin.site.register(OrderItem)
