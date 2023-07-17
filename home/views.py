from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
import braintree
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Category,Product
import json

def productPage(request,id,slug):
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
    except(Exception):
        print("errore in view : generazione token")
    products = Products.objects.filter(available=True)    
    template="product/product.html"    
    products = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)
    return render(request,template,{'products': products,"client_token":client_token})

def product_list(request,category_slug=None):
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
    except(Exception):
        print("errore in view : generazione token")
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)   
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
    template="product/product.html"    
    return render(request,template,{'products': products,"client_token":client_token})

@csrf_exempt
def page(request):
    paymethod = ""
    amount = ""
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
        print("generato Token con chiave ="+client_token)
    except(Exception):
        print("errore in view : generazione token")
    if request.method == 'GET':
        data = json.dumps({"client_token": client_token,})
        return JsonResponse(data, safe=False)
    else:
        if 'amount' in request.POST:
            amount = request.POST['amount']
            print("amount="+amount)
        if 'paymentMethodNonce' in request.POST:
            paymethod = request.POST['paymentMethodNonce']
            print("result="+result)
            result = gateway.transaction.sale({'amount': amount, 'payment_method_nonce': paymethod})
    transaction = str(result.transaction.processor_response_text)
    return HttpResponse(transaction)

#processo di checkout
@csrf_exempt
def checkout(request):
    if 'amount' in request.POST:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        amount = request.POST['amount']
        print("amount="+amount)
    if 'paymentMethodNonce' in request.POST:
        paymethod = request.POST['paymentMethodNonce']
        result = gateway.transaction.sale({'amount': amount, 'payment_method_nonce': paymethod})
        transaction = str(result.transaction.processor_response_text)
        return HttpResponse(transaction)