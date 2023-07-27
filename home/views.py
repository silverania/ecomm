from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import braintree
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
import json
import urllib3
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


def productPage(request, id, slug):
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
    except(Exception):
        print("errore in view : generazione token")
    products = Products.objects.get(available=True)
    template = "product/product.html"
    products = get_object_or_404(Product,
                                 id=id,
                                 slug=slug,
                                 available=True)
    return render(request, template, {'products': products, "client_token": client_token})


''' verifica la presenza di product e altro '''


def serializer(data):
    datas = serializers.serialize(
        "json",
        data,
        cls=LazyEncoder,
        # safe=False,
        use_natural_primary_keys=True,
        use_natural_foreign_keys=True,
    )
    return datas


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return str(obj)
        if isinstance(obj, Category.__class__) or isinstance(obj, Product.__class__):
            return obj
        return super().default(obj)


def product_list(request, category_slug=None):
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
    except(Exception):
        print("errore in view : generazione token")
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = category.products.all()
        nej = serializers.serialize("json", products)
    template = "product/product.html"
    return render(request, template, {"category": category, "client_token": client_token, "categories": categories, "products": nej})


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
        data = json.dumps({"client_token": client_token, })
        return JsonResponse(data, safe=False)
    else:
        if 'amount' in request.POST:
            amount = request.POST['amount']
            print("amount="+amount)
        if 'paymentMethodNonce' in request.POST:
            paymethod = request.POST['paymentMethodNonce']
            print("result="+result)
            result = gateway.transaction.sale(
                {'amount': amount, 'payment_method_nonce': paymethod})
    transaction = str(result.transaction.processor_response_text)
    return HttpResponse(transaction)

# processo di checkout


@csrf_exempt
def checkout(request):
    if 'amount' in request.POST:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        amount = request.POST['amount']
        print("amount="+amount)
    if 'paymentMethodNonce' in request.POST:
        paymethod = request.POST['paymentMethodNonce']
        result = gateway.transaction.sale(
            {'amount': amount, 'payment_method_nonce': paymethod})
        transaction = str(result.transaction.processor_response_text)
        return HttpResponse(transaction)
