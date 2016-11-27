import uuid
import cgi
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transaction_api import TransactionApi
from squareconnect.apis.customer_api import CustomerApi
from app.models import InventoryItem, Invoice, OrderItem

access_token = 'sandbox-sq0atb-0dMkHE4SNy91WlknE8S6Ig'

def charge(request):
    r = request.POST
    nonce = r['nonce']
    location_id = 'CBASECSHZryawv4Lm4P10p3gSj4'
    api_instance = TransactionApi()
    idempotency_key = str(uuid.uuid1())
    print(r)
    invoice = Invoice.objects.create(customer=r['customer'])
    invoice.save()
    form_number = 0

    for x in range(int(r['form-TOTAL_FORMS'])):
        OrderItem.objects.create(invoice=invoice, item = InventoryItem.objects.get(id=int(r['form-{}-item'.format(form_number)])),
                            quantity=int(r['form-{}-quantity'.format(form_number)]),
                            amount=r['form-{}-amount'.format(form_number)],
                            grind=r['form-{}-grind'.format(form_number)])
        form_number += 1

    total_cost = invoice.total_cost * 100
    amount = {'amount': int(total_cost), 'currency': 'USD'}
    body = {'idempotency_key': idempotency_key, 'card_nonce': nonce, 'amount_money': amount}

    try:
      api_response = api_instance.charge(access_token, location_id, body)
      res = api_response.transaction
    except ApiException as e:
      res = "Exception when calling TransactionApi->charge: {}".format(e)


def create_customer(request):
    print(r)
    api_instance = CustomerApi()
    body = {'given_name': r['given_name'], 'company_name': r['company_name'] ,
            'email_address': r['email_address'] , 'phone_number': r['phone_number'] ,'note': r['note']}
    try:
      api_response = api_instance.create_customer(access_token, body)
      res = api_response.customer
    except ApiException as e:
      res = "Exception when calling CustomerApi->create: {}".format(e)


def list_customers():
    api_instance = CustomerApi()
    api_response = api_instance.list_customers(access_token)
    return api_response.customers

def delete_customer(customer_id):
    api_instance = CustomerApi()
    api_response = api_instance.delete_customer(access_token, customer_id)

def update_customer(customer_id, request):
    api_instance = CustomerApi()
    r = request.POST
    body = {'given_name': r['given_name'], 'company_name': r['company_name'] ,
            'email_address': r['email_address'] , 'phone_number': r['phone_number'] ,'note': r['note']}
    api_response = api_instance.update_customer(access_token, customer_id, body)
