from rest_framework import serializers
from .models import Product, Order, OrderItem, User
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "is_staff",
            "is_superuser",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "stock",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    items = OrderItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ("status", "items", "order_id", "user")
        extra_kwargs = {
            "user": {"read_only": True},
            "order_id": {"read_only": True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                product = item_data["product"]
                quantity = item_data["quantity"]
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity
                )
        return order

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop("items")

        with transaction.atomic():

            instance = super().update(instance, validated_data)
            if orderitem_data is not None:
                instance.items.all().delete()

                for item in orderitem_data:
                    product = item["product"]
                    quantity = item["quantity"]
                    OrderItem.objects.create(
                        order=instance, product=product, quantity=quantity
                    )

        return instance


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    order_id = serializers.UUIDField(read_only=True)

    def total(self, obj):
        order_items = obj.items.all()
        total = 0
        for item in order_items:
            total += item.item_subtotal
        return total

    class Meta:
        model = Order
        fields = ("order_id", "user", "status", "created_at", "items", "total_price")


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
