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

from django.urls import path, include
from home import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/<slug:category_slug>/<slug:product_slug>',
         views.product_list, name="product_list"),
    path('admin', admin.site.urls),
    path('<int:id>/<slug:slug>/', views.productPage,
         name='productPage'),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session),  # new
    path('success/', views.SuccessView.as_view()),  # new
    path('cancelled/', views.CancelledView.as_view()),  # new
    path('webhook/', views.stripe_webhook),  # new
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
