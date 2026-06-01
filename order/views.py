from django.shortcuts import render, redirect
from django.views import View
from .models import Order
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CheckOutView(LoginRequiredMixin, View):
    redirect_field_name = "next"
    
    def get(self, request):
        total = 0
        for item in request.user.cart.cart_item.all():
            total += item.get_price()
        return render(request, "order/checkout.html", { "total": round(total, 2) })
    
    def post(self, request):
        total_amount = 0
        order = Order.objects.create(user=request.user)
        order.save()

        for item in request.user.cart.cart_item.all():
            ordet_item = order.order_item.create(product=item.product, quantity=item.quantity) # type: ignore
            total_amount += item.get_price()
            ordet_item.save()
        
        order.total_amount = total_amount
        order.status = Order.Status.DELIVERD
        order.save()
        messages.success(request, "Thank you for your purchase")
        return redirect("product:clear_cart")