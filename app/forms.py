
from django import forms
from app.models import InventoryItem, OrderItem
from django.forms import ModelChoiceField
from app.square_functions import list_customers, access_token

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

    SIZE = [

    ("12","12oz"),
    ("16", "1lbs"),
    ("80", "5lbs")

    ]


    item = MyModelChoiceField(queryset=InventoryItem.objects.all(), empty_label=None)
    quantity = forms.IntegerField(initial=0, min_value=0)
    amount = forms.ChoiceField(choices=SIZE)
    grind = forms.ChoiceField(choices=GRIND)

class CustomerForm(forms.Form):

    DISCOUNT = [
    ("Discount","Discount"),
    ("No Discount", "No Discount"),
    ]

    given_name = forms.CharField()
    company_name = forms.CharField(required=False)
    email_address = forms.EmailField()
    phone_number = forms.CharField(required=False)
    discount = forms.ChoiceField(choices=DISCOUNT)
