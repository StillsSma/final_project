from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from app.models import InventoryItem, Profile, OrderItem, Invoice
from app.forms import OrderItemForm, CustomerForm,InvoiceCustomerForm
from django.forms import formset_factory
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from app.square_functions import charge, create_customer,list_customers, delete_customer, access_token
from django.shortcuts import redirect


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
    success_url = reverse_lazy('index_view')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class CustomerServiceTemplateView(TemplateView):
    template_name = "customer_service.html"

    def get_context_data(self, **kwargs):
        context = {}

        return context


class CustomerFormView(FormView):
    template_name = "customer_form.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customer_service_view")

    def form_valid(self, form):
        create_customer(self.request)
        return super(CustomerFormView, self).form_valid(form)

class CustomerListView(ListView):
    template_name = "customer_list.html"
    def get_queryset(self):
        return list_customers()

def customer_delete_view(request, customer_id):
    delete_customer(customer_id)
    return render(request, 'customer_list.html')





class InvoiceSeen(UpdateView):
    model = Invoice
    fields = ("roaster_seen", "production_seen", "shipping_seen",)

    def form_valid(self, form):
        if self.request.user.profile.access_level == 'r':
            instance = form.save(commit=False)
            instance.roaster_seen = True
        if self.request.user.profile.access_level == 'p':
            instance = form.save(commit=False)
            instance.production_seen = True
        if self.request.user.profile.access_level == 'd':
            instance = form.save(commit=False)
            instance.shipping_seen = True
        return super().form_valid(form)

    def get_success_url(self):
        print(self.request.GET['next'])
        if 'next' in self.request.GET:
            return self.request.GET['next']



class OrderItemFormView(FormView):
    template_name = "credit_card.html"

    def get_context_data(self, **kwargs):
        context = {}
        OrderItemFormSet = formset_factory(OrderItemForm)
        context['formset'] = OrderItemFormSet
        context['invoice_form'] = InvoiceCustomerForm

        return context


class IndexView(ListView):
    model = Invoice

class InventoryListView(ListView):
    model = InventoryItem

class InventoryCreateView(CreateView):
    model = InventoryItem
    fields = ['name', 'price_12_oz', 'price_1_lbs', 'price_5_lbs']
    success_url = reverse_lazy("inventory_list_view")

class InventoryUpdateView(UpdateView):
    model = InventoryItem
    fields = ['name', 'price_12_oz', 'price_1_lbs', 'price_5_lbs']
    success_url = reverse_lazy("inventory_list_view")

class InventoryDeleteView(DeleteView):
    model = InventoryItem
    success_url = reverse_lazy("inventory_list_view")

class RoastingListView(ListView):
    model = Invoice
    template_name = "app/roasting.html"

    def get_queryset(self):
        invoices = super(RoastingListView, self).get_queryset()
        return invoices.filter(roaster_complete=False)

class ProductionListView(ListView):
    model = Invoice
    template_name = "app/production.html"

    def get_queryset(self):
        invoices = super(ProductionListView, self).get_queryset()
        return invoices.filter(production_complete=False)

class DeliveryListView(ListView):
    model = Invoice
    template_name = "app/delivery.html"

    def get_queryset(self):
        invoices = super(DeliveryListView, self).get_queryset()
        return invoices.filter(production_complete=False)


def process_view(request):
    if request.method == 'POST':
        if 'add_item' in request.POST:
            OrderItemFormSet = formset_factory(OrderItemForm)
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS'])+ 1
            new_formset = OrderItemFormSet(cp, prefix='form')
            return render(request, 'credit_card.html', {'formset':new_formset, 'invoice_form':InvoiceCustomerForm})
        else:
            charge(request)
            return render(request, 'process.html')
