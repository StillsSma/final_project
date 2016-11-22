from django import forms
from app.models import InventoryItem, OrderItem
from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class OrderItemForm(forms.Form):
    GRIND = [
    ("whole bean", "WB" ),
    ("fine", "#3"),
    ("standard", "#7"),
    ("coarse", "#10")

    ]
    item = MyModelChoiceField(queryset=InventoryItem.objects.all(), empty_label=None)
    quantity = forms.IntegerField()
    description = forms.CharField()
    grind = forms.ChoiceField(choices=GRIND)
