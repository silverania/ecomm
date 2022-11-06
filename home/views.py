from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import braintree
from django.conf import settings


def page(request):
    paymethod = ""
    amount = ""
    cardNumberValue = ""
    expiration_date = ""
    gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
    if request.method == 'GET':
        return render(request, "base_ecomm.html")
# per il client_token invece che la token_key :
# client_token = gateway.client_token.generate()
# return render(request, "base_ecomm.html" , {'client_token' : client_token})
    else:
        request.method == 'POST'
        if 'amount' in request.POST:
            amount = request.POST['amount']
        if 'paymentMethodNonce' in request.POST:
            paymethod = request.POST['paymentMethodNonce']
        if 'cardNumberValue' in request.POST:
            cardNumberValue = request.POST['cardNumberValue']
    result = gateway.transaction.sale({"credit_card": {
                                                      "number": cardNumberValue,
                                                      "expiration_date": "05/2010",
        "cvv": "100"
    },
                                        {'amount': amount, 'payment_method_nonce': paymethod,
                                         'options':                                           {'submit_for_settlement': True, }})
        if result.is_success:
        print(str(result))
        return HttpResponse({'result': result})
        HttpResponse("Qualcosa è andato storto", {'result': result})
