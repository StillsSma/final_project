from django.shortcuts import render
from django.urls import reverse_lazy
from app.models import InventoryItem
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView



class TransactionView(TemplateView):
    template_name = "index.html"

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
