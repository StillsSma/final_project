from django import forms
from app.models import InventoryItem
from django.forms import ModelChoiceField

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name



class OrderForm(forms.Form):
    name = MyModelChoiceField(queryset=InventoryItem.objects.all(), empty_label=None)
    quantity = forms.IntegerField()
