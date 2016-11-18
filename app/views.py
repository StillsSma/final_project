from django.shortcuts import render
from django.urls import reverse_lazy
from app.models import InventoryItem
from app.forms import OrderForm
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from app.charge_card import charge


class TransactionView(FormView):
    template_name = "credit_card.html"
    form_class = OrderForm


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
        charge(request)

    return render(request, 'process.html')
