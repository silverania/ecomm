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
from celery import shared_task
from ecomm.tasks import order_created


def productPage(request, id, slug):
    #gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
    #client_token = gateway.client_token.generate()
    products = Products.objects.get(available=True)
    template = "product/product.html"
    products = get_object_or_404(Product,
                                 id=id,
                                 slug=slug,
                                 available=True)
    return render(request, template, {'products': products})


''' verifica la presenza di product e altro '''


def serializer(data):
    datas = serializers.serialize(
        "json",
        data,
        cls=LazyEncoder,
        safe=False,
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


def product_list(request, category_slug=None, product_slug=None):
    try:
        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
        client_token = gateway.client_token.generate()
    except(Exception):
        print("errore in view : generazione token")
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category_selected = str(category_slug)
        category = Category.objects.filter(slug=category_slug)
        cat = Category.objects.get(name=category_selected)
        products = cat.products.all()
        nej = serializers.serialize("json", products)
        cat = list(category)
        category = serializers.serialize("json", cat)
    if product_slug:
        for p in products:
            if p.slug == product_slug:
                product = Product.objects.get(slug=product_slug)
    template = "product/product.html"
    return render(request, template, {"categories": categories, "category_selected": category_selected, "product": product, "cat": cat, "client_token": client_token, "products": nej})


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
            breakpoint()
        if 'paymentMethodNonce' in request.POST:
            paymethod = request.POST['paymentMethodNonce']
            print("result="+result)
            result = gateway.transaction.sale(
                {'amount': amount, 'payment_method_nonce': paymethod})
            breakpoint()
    transaction = str(result.transaction.processor_response_text)
    order_created.delay(order.id)
    breakpoint()
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
            {'amount': amount, 'payment_method_nonce': paymethod, "options": {
                "submit_for_settlement": True}})
        transaction = str(result.transaction.processor_response_text)
    return JsonResponse({"transaction": transaction, "result.is_success": result.is_success})
