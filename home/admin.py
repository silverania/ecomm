from django.contrib import admin
from .models import Category, Product, Manager


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'idapi', 'slug', 'price', 'consegna',
                    'available', 'created', 'updated']
    list_filter = ['available', 'idapi', 'created', 'updated', 'consegna']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
