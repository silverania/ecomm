"""ecomm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from paypal.pro.helpers import PayPalWPP
from django.urls import path, include
from home import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/<slug:category_slug>/<slug:product_slug>',
         views.product_list, name="product_list"),
    path('page', views.page),
    path('admin', admin.site.urls),
    path('<int:id>/<slug:slug>/', views.productPage,
         name='productPage'),
    path('payment-url/', views.checkout),
    path('paypal/', include('paypal.standard.ipn.urls')),
    #path('checkout/', views.checkout),

    path('checkout/', views.payment_checkout, name='checkout_payment'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('execute_payment/payment_failed.html',
         views.execute_payment, name='payment_failed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
