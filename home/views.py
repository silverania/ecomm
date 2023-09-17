from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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
product = Product.objects


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
    global product

    def checkDisponibility(root):
        headers = headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            response = requests.get(root, headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            response.encoding = 'utf-8'  # Optional: requests infers this internally
            soup = BeautifulSoup(response.text)
            span = soup.find_all(
                'span', {'class': 'a-color-price a-text-bold'})
            print(span)
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
            print(p)
            checkDisponibility(p.rootLink)
    template = "product/product.html"
    return render(request, template, {"categories": categories, "category_selected": category_selected, "product": product, "cat": category, "products": nej})


@ csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(stripe_config, safe=False)


@ csrf_exempt
def create_checkout_session(request, product_slug=None):
    global product
    if request.method == 'GET':
        domain_url = 'https://127.0.0.1:8000/home/animali/borraccia-portatile/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # PRENDI I WEBHOOKS NEL TERMNALE COSÌ : stripe listen --forward-to localhost:8000/webhook/
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': product.idapi
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


@ csrf_exempt
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
