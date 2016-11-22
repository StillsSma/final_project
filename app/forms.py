from django.forms import ModelForm
from app.models import InventoryItem, OrderItem
from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['invoice']
