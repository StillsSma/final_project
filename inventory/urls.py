
from django.conf.urls import url, include
from django.contrib import admin
from app.views import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView, OrderItemFormView, \
                        UserCreateView, ProfileUpdateView, RoastingListView, ProductionListView, DeliveryListView, process_view, \
                        IndexView, CustomerServiceTemplateView, CustomerFormView, CustomerListView, customer_delete_view, \
                        customer_update_view, invoice_update_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^customer_service/$', CustomerServiceTemplateView.as_view(), name="customer_service_view"),
    url(r'^customer_service/create$', CustomerFormView.as_view(), name="customer_form_view"),
    url(r'^customer_service/list$', CustomerListView.as_view(), name="customer_list_view"),
    url(r'^customer_service/update/(?P<customer_id>.*)$', customer_update_view, name="customer_update_view"),
    url(r'^customer_service/delete/(?P<customer_id>.*)$', customer_delete_view, name="customer_delete_view"),
    url(r'^customer_service/inventory$', InventoryListView.as_view(), name="inventory_list_view"),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^accounts/profile/$', ProfileUpdateView.as_view(), name="profile_update_view"),
    url(r'^create/$', InventoryCreateView.as_view(), name="inventory_create_view"),
    url(r'^update/(?P<pk>\d+)$', InventoryUpdateView.as_view(), name="inventory_update_view"),
    url(r'^delete/(?P<pk>\d+)$', InventoryDeleteView.as_view(), name="inventory_delete_view"),
    url(r'^order/$', OrderItemFormView.as_view(), name="order_form_view"),
    url(r'^process_card/$',process_view, name="process_view"),
    url(r'^invoice/(?P<pk>\d+)$', invoice_update_view, name="invoice_update_view"),
    url(r'^roasting/$', RoastingListView.as_view(), name="roasting_list_view"),
    url(r'^production/$', ProductionListView.as_view(), name="production_list_view"),
    url(r'^delivery/$', DeliveryListView.as_view(), name="delivery_list_view")


    ]
