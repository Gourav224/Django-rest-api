from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import (
    ProductSerializer,
    OrderSerializer,
    ProductInfoSerializer,
)
from api.models import Product, Order
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(["GET"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def product_detail(reqquest, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def orders_list(request):
    orders = Order.objects.prefetch_related("items__product")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)
