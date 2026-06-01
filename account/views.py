from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from product.models import Cart
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    def get(self, request):
        return render(request, "account/register.html")

    def post(self, request):
        if errors := self.validate_data(request.POST):
            return render(request, "account/register.html", { "errors": errors, "data": request.POST })
        
        user = User.objects.create_user(
            username = request.POST["username"],
            email= request.POST["email"],
            password = request.POST["password"],
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"]
            )
        user.save()
        Cart.objects.create(user=user).save()
        messages.success(request, "Registerer Successfully")
        return redirect("account:login")
    
    def validate_data(self, data):
        errors = []
        if len(str(data["username"]).strip()) < 2: errors.append("Username is too short")
        if len(str(data["first_name"]).strip()) < 2: errors.append("Firstname is too short")
        if len(str(data["last_name"]).strip()) < 2: errors.append("Lastname is too short")
        if len(str(data["password"]).strip()) < 8: errors.append("password must be more than 7 characters long")
        if data["password"] != data["password_confirm"]: errors.append("passwords don't match")
        return errors
        

class DashboardView(LoginRequiredMixin, View):
    redirect_field_name = "next"
    def get(self, request):
        total = 0
        user = User.objects.get(pk=request.user.pk)
        for item in user.cart.cart_item.all(): # type: ignore
            total += item.get_price()
        return render(request, "account/dashboard.html", { "user": user, "total": round(total, 2) })