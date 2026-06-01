from django.urls import path
from . import views


app_name = "product"
urlpatterns = [
    path("", views.ProductList.as_view(), name="product_list"),
    path("platform/<slug:slug>/products", views.PlatformList.as_view(), name="platform_product"),
    path("products/<slug:slug>/", views.ProductDetail.as_view(), name="product_detail"),
    path("products/<slug:slug>/cart/", views.AddToCart.as_view(), name="add_to_cart"),
    path("cart/item/<int:pk>/operation", views.ItemOperation.as_view(), name="item_inc"),
    path("cart/item/<int:pk>/remove", views.ItemRemove.as_view(), name="item_remove"),
    path("cart/clear", views.ClearCart.as_view(), name="clear_cart"),
]