from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Category, Client, Order
# Register your models here.

@admin.action(description="Add 50 to the product's current stock")
def load_stock(modeladmin, request, queryset):
    for product in queryset:
        product.stock = product.stock + 50
        product.save()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category', 'stock', 'available'] #FIELDS TO DISPLAY
    actions = [load_stock]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'city']  #FIELDS TO DISPLAY

admin.site.register(Category)
admin.site.register(Order)