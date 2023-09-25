from collections import OrderedDict
from .models import OrderItem, Order
from .forms import OrderCreateForm
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Category, Product
import json
import urllib3
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from celery import shared_task
from ecomm.tasks import order_created
import stripe
from django.views.generic import TemplateView
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


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


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'product/detail.html', {'product': product})


def product_list(request, category_slug=None, product_slug=None):
    template = "list.html"
    product = Product()
    product_slug = product_slug
    category_selected = ""
    category_slug = category_slug
    products = Product.objects.all()
    nej = Product()
    category = Category.objects.all()
    product_slug = product_slug
    cat = ""
    categories = Category.objects.all()
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
            print(p)
    else:
        products = Product.objects.filter(disponibile=True)
        return render(request, template, {"categories": categories, "category_selected": category_selected,
                                          "productid": product.id, "product": product, "cat": category, "products": products})
    return render(request, template, {"categories": categories, "category_selected": category_selected,
                                      "productid": product.id, "product": product, "cat": category, "products": nej})


def homeecomm(request):
    template = "homeecomm.html"
    return render(request, template)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, productid=None):
    stripe_account = "acct_1NolN0AChwTB2ifJ"
    if productid:
        product = Product.objects.get(id=productid)
    #data = json.loads(request.POST.get('data3'))
    #prodottoid = data['productid']
    if request.method == 'GET':
        domain_url = 'https://127.0.0.1:8000/home/animali/'+product.slug
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                # PRENDI I WEBHOOKS NEL TERMNALE COSÌ : stripe listen --forward-to localhost:8000/webhook/
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + "/success/success.html" +
                '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': product.idapi,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get(self, request, category_slug=None, product_slug=None):
        if product_slug:
            product = Product.objects.get(slug=product_slug)
        return render(request, self.template_name, {'product': product.consegna})


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here
    return HttpResponse(status=200)


@csrf_exempt
def infoacquisto(request):
    ordine = Order()
    data = json.loads(request.POST['data3'])
    ordine.cognome = data['cognome']
    ordine.nome = data['nomeuser']
    ordine.telefono = data['telefono']
    ordine.città = data['citta']
    ordine.postal = data['cap']
    ordine.infovarie = data['infoerichieste']
    ordine.via = data['via']
    ordine.civico = data['civico']
    prodottoid = Product.objects.get(id=data['productid'])
    ordine.prodotto = prodottoid
    ordine.save()

    return HttpResponse(status=200)


@csrf_exempt
def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderItem.objects.create(order=order, product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
# clear the cart
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(request,  'orders/order/create.html', {'cart': cart, 'form': form})
