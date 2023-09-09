from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
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
from paypal.pro.views import PayPalPro


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
    return render(request, template, {"categories": categories, "category_selected": category_selected, "product": product, "cat": cat, "products": nej})


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


def nvp_handler(nvp):
    # This is passed a PayPalNVP object when payment succeeds.
    # This should do something useful!
    pass


@csrf_exempt
def checkout(request):
    breakpoint()

    return ppp(request)


def create_billing_agreement_view(request):
    wpp = PayPalWPP(request)
    token = request.GET.get('token')
    wpp.createBillingAgreement({'token': token})


def do_reference_transaction_view(request):
    wpp = PayPalWPP(request)
    reference_id = request.POST.get('reference_id')
    amount = request.POST.get('amount')
    wpp.doReferenceTransaction({'referenceid': reference_id, 'amt': amount})


def checkout(request):
    item = {"paymentrequest_0_amt": "0.1",  # amount to charge for item
            "inv": "inventory",         # unique tracking variable paypal
            "custom": "tracking",       # custom tracking variable for you
            "cancelurl": "http://...",  # Express checkout cancel url
            "returnurl": "http://..."}  # Express checkout return url
    ppp = PayPalPro(
        item=item,                            # what you're selling
        payment_template="payment.html",      # template name for payment
        confirm_template="confirmation.html",  # template name for confirmation
        success_url="/success/",              # redirect location after success
        nvp_handler=nvp_handler)
    return ppp(request)
