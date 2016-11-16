from django.shortcuts import render
from django.urls import reverse_lazy
from app.models import InventoryItem
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import cgi
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transaction_api import TransactionApi



class TransactionView(TemplateView):
    template_name = "credit_card.html"

class InventoryListView(ListView):
    model = InventoryItem

class InventoryCreateView(CreateView):
    model = InventoryItem
    fields = ['name', 'price', 'quantity']
    success_url = reverse_lazy("inventory_list_view")

class InventoryUpdateView(UpdateView):
    model = InventoryItem
    fields = ['name', 'price', 'quantity']
    success_url = reverse_lazy("inventory_list_view")

class InventoryDeleteView(DeleteView):
    model = InventoryItem
    success_url = reverse_lazy("inventory_list_view")

def process_view(request):
    if request.method == 'POST':

        nonce = request.POST['nonce']
        access_token = 'sandbox-sq0atb-0dMkHE4SNy91WlknE8S6Ig'
        location_id = 'CBASECSHZryawv4Lm4P10p3gSj4'
        api_instance = TransactionApi()
        idempotency_key = str(uuid.uuid1())
        amount = {'amount': 100, 'currency': 'USD'}
        body = {'idempotency_key': idempotency_key, 'card_nonce': nonce, 'amount_money': amount}

        try:
          api_response = api_instance.charge(access_token, location_id, body)
          res = api_response.transaction
        except ApiException as e:
          res = "Exception when calling TransactionApi->charge: {}".format(e)
        item = InventoryItem.objects.get(pk=3)
        item.quantity = item.quantity - 1
        item.save()

    return render(request, 'process.html')
