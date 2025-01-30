from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product
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
