from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from app.models import InventoryItem, Profile, OrderItem, Invoice
from app.forms import OrderItemForm, CustomerForm
from django.forms import formset_factory
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from app.square_functions import charge, create_customer, update_customer, list_customers, \
                                retrieve_customer, delete_customer, sandbox_access_token, access_token
from django import forms
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
        object_list = Invoice.objects.all()
        context = {'invoices': object_list}

        return context


class CustomerFormView(FormView):
    template_name = "customer_form.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customer_service_view")

    def form_valid(self, form):
        print(self.request.POST)
        create_customer(self.request)
        return super(CustomerFormView, self).form_valid(form)

class CustomerListView(ListView):
    template_name = "customer_list.html"
    def get_queryset(self):
        return list_customers()


def customer_update_view(request, customer_id):
    c = retrieve_customer(customer_id)
    form = CustomerForm(initial={'given_name': c.given_name, 'company_name': c.company_name,
                                'email_address': c.email_address, 'phone_number': c.phone_number,
                                'discount': c.note})
    if request.method == 'GET':
        return render(request, "customer_form.html", {'form': form})
    else:
        update_customer(customer_id, request)
        return redirect('customer_list_view')

def customer_delete_view(request, customer_id):

    delete_customer(customer_id)
    return redirect('customer_list_view')

def invoice_update_view(request, pk):
    invoice = Invoice.objects.get(id=pk)
    if request.user.profile.access_level == 'r':
        if invoice.roaster_seen == False:
            invoice.roaster_seen = True
        else:
            invoice.roaster_complete = True
    elif request.user.profile.access_level == 'p':
            if invoice.production_seen == False:
                invoice.production_seen = True
            else:
                invoice.production_complete = True
    elif request.user.profile.access_level == 'd':
            if invoice.shipping_seen == False:
                invoice.shipping_seen = True
            else:
                invoice.shipping_complete = True

    if 'next' in request.GET:
         print(request.GET['next'])
    invoice.save()
    return redirect(request.META['HTTP_REFERER'])


def order_item_view(request):
    class InvoiceCustomerForm(forms.Form):
        CUSTOMERS = []
        try:
            for customer in list_customers():
                result = [customer.id, (customer.given_name + ' ' + str(customer.email_address)) ]
                CUSTOMERS.append(tuple(result))
        except TypeError:
            CUSTOMERS = []
        customer = forms.ChoiceField(choices=CUSTOMERS)
        delivery = forms.BooleanField()
    OrderItemFormSet = formset_factory(OrderItemForm)
    if request.method == 'GET':
        return render(request, 'credit_card.html', {'formset': OrderItemFormSet, 'invoice_form': InvoiceCustomerForm} )
    else:
        if 'add_item' in request.POST:
            OrderItemFormSet = formset_factory(OrderItemForm)
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS'])+ 1
            new_formset = OrderItemFormSet(cp, prefix='form')
            return render(request, 'credit_card.html', {'formset':new_formset, 'invoice_form':InvoiceCustomerForm})
        else:
            charge(request)
            return redirect('customer_service_view')

class IndexView(ListView):
    model = Invoice

class InventoryListView(ListView):
    model = InventoryItem

class InventoryCreateView(CreateView):
    model = InventoryItem
    fields = ['name', 'picture', 'price_12_oz', 'price_1_lbs', 'price_5_lbs']
    success_url = reverse_lazy("inventory_list_view")

class InventoryUpdateView(UpdateView):
    model = InventoryItem
    fields = ['name', 'picture', 'price_12_oz', 'price_1_lbs', 'price_5_lbs']
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
        return invoices.filter(shipping_complete=False, delivery=True)
