from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from app.models import InventoryItem, Profile, OrderItem, Invoice
from app.forms import OrderItemForm
from django.forms import formset_factory
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from app.charge_card import charge

class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy("profile_update_view")
    form_class = UserCreationForm
    def form_valid(self, form): #logs the user in upon account creation
        valid = super(UserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class ProfileUpdateView(UpdateView):
    template_name = "profile.html"
    fields = ("access_level",)
    success_url = reverse_lazy('inventory_list_view')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class OrderItemFormView(FormView):
    template_name = "credit_card.html"
    form_class = OrderItem

    def get_context_data(self, **kwargs):
        context = {}
        OrderItemFormSet = formset_factory(OrderItemForm)
        context['formset'] = OrderItemFormSet

        return context

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

class RoastingListView(ListView):
    model = Invoice
    template_name = "app/roasting.html"

    def get_queryset(self):
        invoices = super(RoastingListView, self).get_queryset()
        return invoices.filter(roaster=False)

class ProductionListView(ListView):
    model = Invoice
    template_name = "app/production.html"

    def get_queryset(self):
        invoices = super(ProductionListView, self).get_queryset()
        return invoices.filter(production=False)

def process_view(request):
    if request.method == 'POST':
        if 'add_item' in request.POST:
            OrderItemFormSet = formset_factory(OrderItemForm)
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS'])+ 1
            new_formset = OrderItemFormSet(cp, prefix='form')
            return render(request, 'credit_card.html', {'formset':new_formset})
        else:
            charge(request)
            return render(request, 'process.html')
