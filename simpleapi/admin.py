from django.contrib import admin
from .models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    """To change view in admin page"""
    list_display = ('product_name', 'stock')
    ordering = ('-stock',)


class OrderAdmin(admin.ModelAdmin):
    """To change view in admin page"""
    list_display = ('source', 'order_id')


class OrderItemAdmin(admin.ModelAdmin):
    """To change view in admin page"""
    list_display = ('product',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
