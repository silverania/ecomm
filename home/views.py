from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


class Product_List(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'product/list.html', {'category': category,
                      'categories': categories, 'products': products})


class Product_Detail(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        return render(request, 'product/detail.html',
                      {'product': product})
