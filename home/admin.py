from .models import Order, OrderItem
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
    list_display = ['name', 'idapi', 'slug', 'price', 'consegna', 'manager',
                    'available', 'created', 'updated']
    list_filter = ['available', 'idapi', 'created',
                   'updated', 'consegna', 'manager']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'cognome', 'email', 'via', 'postal', 'città', 'pagato',
                    'creato', 'updated']
    list_filter = ['pagato', 'creato', 'updated']
    inlines = [OrderItemInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
