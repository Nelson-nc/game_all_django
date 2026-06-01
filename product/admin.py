from django.contrib import admin

from .models import Product, Cart, CartItem, Platform


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Platform)
admin.site.register(Product)