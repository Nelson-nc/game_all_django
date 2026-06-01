from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Platform(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=10)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:platform", kwargs={"slug": self.slug})
    
    

class Product(models.Model):
    image = models.ImageField(upload_to="products")
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0.00) # type: ignore
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=20)
    stock_quantity = models.IntegerField(default=0)
    platforms = models.ManyToManyField(Platform, related_name="product")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.slug})
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"""
        Qty: {self.quantity}, 
        Product: {self.product.name}, 
        Price (qxp.p): {self.product.price*self.quantity}
    """

    def get_price(self) -> float:
        return round(float(self.product.price) * float(self.quantity), 2)