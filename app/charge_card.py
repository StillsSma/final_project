import uuid
import cgi
import squareconnect
from squareconnect.rest import ApiException
from squareconnect.apis.transaction_api import TransactionApi
from app.models import InventoryItem, Invoice, OrderItem

def charge(request):
    r = request.POST
    nonce = r['nonce']
    access_token = 'sandbox-sq0atb-0dMkHE4SNy91WlknE8S6Ig'
    location_id = 'CBASECSHZryawv4Lm4P10p3gSj4'
    api_instance = TransactionApi()
    idempotency_key = str(uuid.uuid1())
    print(r['form-TOTAL_FORMS'])

    print("++++++++++++++++++++++++++++++")
    #total_cost = int(r['quantity']) * InventoryItem.objects.get(id=r['name']).price * 100

    #amount = {'amount': int(total_cost), 'currency': 'USD'}
    #body = {'idempotency_key': idempotency_key, 'card_nonce': nonce, 'amount_money': amount}

    #try:
    #  api_response = api_instance.charge(access_token, location_id, body)
    #  res = api_response.transaction
    #except ApiException as e:
    #  res = "Exception when calling TransactionApi->charge: {}".format(e)

    invoice = Invoice.objects.create()
    invoice.save()
    form_number = 0
    for x in range(int(r['form-TOTAL_FORMS'])):
        OrderItem.objects.create(invoice=invoice, item = r['form-{}-item'.format(form_number)],
                            quantity=int(r['form-{}-quantity'.format(form_number)]),
                            description=r['form-{}-description'.format(form_number)],
                            grind=r['form-{}-grind'.format(form_number)])
        form_number += 1
