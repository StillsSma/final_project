"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView, TransactionView, process_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', InventoryListView.as_view(), name="inventory_list_view"),
    url(r'^create/$', InventoryCreateView.as_view(), name="inventory_create_view"),
    url(r'^update/(?P<pk>\d+)$', InventoryUpdateView.as_view(), name="inventory_update_view"),
    url(r'^delete/(?P<pk>\d+)$', InventoryDeleteView.as_view(), name="inventory_delete_view"),
    url(r'^transaction/$', TransactionView.as_view(), name="transaction_view"),
    url(r'^process_card/$',process_view, name="process_view"),


    ]
