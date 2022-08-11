from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


class HomePage(View):
    def get(self, request):
        template = "product/list.html"
        return render(request, template)


class Product_List(View):
    def product_list(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'shop/product/list.html', {'category': category,
                      'categories': categories, 'products': products})


class Product_Detail(View):
    def product_detail(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        return render(request, 'shop/product/detail.html',
                      {'product': product})
