from django.contrib import admin

# Register your models here.
from app.models import InventoryItem

admin.site.register(InventoryItem)
