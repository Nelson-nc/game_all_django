from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, DashboardView


app_name = "account"
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="account/login.html", next_page="product:product_list"), name="login"),
    path("logout/", LogoutView.as_view(next_page="product:product_list"), name="logout"),
]