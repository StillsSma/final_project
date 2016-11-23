from django.forms import ModelForm
from app.models import InventoryItem, OrderItem
from django.forms import ModelChoiceField



class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['invoice',]
