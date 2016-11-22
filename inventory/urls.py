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
from django.conf.urls import url, include
from django.contrib import admin
from app.views import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView, OrderItemFormView, \
                        UserCreateView, ProfileUpdateView, RoastingListView, ProductionListView, process_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^roasting/inventory$', InventoryListView.as_view(), name="inventory_list_view"),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^accounts/profile/$', ProfileUpdateView.as_view(), name="profile_update_view"),
    url(r'^create/$', InventoryCreateView.as_view(), name="inventory_create_view"),
    url(r'^update/(?P<pk>\d+)$', InventoryUpdateView.as_view(), name="inventory_update_view"),
    url(r'^delete/(?P<pk>\d+)$', InventoryDeleteView.as_view(), name="inventory_delete_view"),
    url(r'^order/$', OrderItemFormView.as_view(), name="order_form_view"),
    url(r'^process_card/$',process_view, name="process_view"),
    url(r'^roasting/$', RoastingListView.as_view(), name="roasting_list_view"),
    url(r'^production/$', ProductionListView.as_view(), name="production_list_view")


    ]
