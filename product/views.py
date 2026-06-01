from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Cart, Platform


class ProductList(View):
    def get(self, request):
        platforms = Platform.objects.all()
        products = Product.objects.all().order_by("?")
        if query := request.GET.get('name'):
            products = products.filter(name__contains=query)
        return render(request, "product/product_list.html", { "products": products, "platforms": platforms })


class PlatformList(View):
    def get(self, request, slug):
        platforms = Platform.objects.all()
        platform = get_object_or_404(Platform, slug=slug)
        products = platform.product.all() # type: ignore
        platform_tag = platform.name
        if query := request.GET.get('name'):
            products = products.filter(name__contains=query)
        context = { "products": products, "platforms": platforms, "platform_tag": platform_tag }
        return render(request, "product/product_list.html", context)


class ProductDetail(View):
    def get(self, request, slug):
        in_cart = False
        product = get_object_or_404(Product, slug=slug)
        if request.user.is_authenticated:
            for item in request.user.cart.cart_item.all():
                if item.product == product:
                    in_cart = True
        return render(request, "product/product_detail.html", { "product": product, "in_cart": in_cart })


class AddToCart(LoginRequiredMixin, View):
    redirect_field_name = "next"

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        if request.user.is_authenticated == False:
            return redirect("account:login")
        
        cart = Cart.objects.get(user=request.user.pk)
        
        if cart is None:
            cart = Cart.objects.create(user=request.user)
            cart.save()

        cart.cart_item.create(product=product).save() # type: ignore
        messages.success(request, f"{product.name} Added to Cart Successfully")
        return redirect(product)


class ItemOperation(LoginRequiredMixin, View):
    redirect_field_name = "next"

    def post(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user.pk)
        item = cart.cart_item.get(pk=pk) # type: ignore
        
        if not item:
            raise Http404("Item not found")
        
        if request.POST["cart_opration"] == "+":
            item.quantity = F("quantity") + 1
        elif request.POST["cart_opration"] == "-":
            if item.quantity <= 1:
                return redirect("product:item_remove", item.pk)
            else:
                item.quantity = F("quantity") - 1
        item.save()
        return redirect("account:dashboard")
            

class ItemRemove(LoginRequiredMixin, View):
    redirect_field_name = "next"

    def get(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user.pk)
        item = cart.cart_item.get(pk=pk) # type: ignore

        if not item:
            raise Http404("Item not found")
        
        item.delete()
        return redirect("account:dashboard")
    

class ClearCart(LoginRequiredMixin, View):
    redirect_field_name = "next"
    
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user.pk)
        for item in cart.cart_item.all(): # type: ignore
            item.delete()
        messages.success(request, "Cart Cleared Successfully")
        return redirect("account:dashboard")
        