import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    tags = models.JSONField(default=list , blank=True , null=True , help_text="List of tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING"
        COMPLETED = "COMPLETED"
        CANCELLED = "CANCELLED"

    order_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Order {self.order.order_id} Item {self.product.name}"
