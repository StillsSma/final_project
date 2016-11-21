from django.contrib import admin

# Register your models here.
from app.models import InventoryItem, Profile, Invoice

admin.site.register(InventoryItem)
admin.site.register(Profile)
admin.site.register(Invoice)
