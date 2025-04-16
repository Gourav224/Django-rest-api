from django.db.models import Max
from api.serializers import (
    ProductSerializer,
    OrderSerializer,
    ProductInfoSerializer,
)
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .filters import InStockFilterBackend, ProductFilter


# Create your views here.


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock"]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)
