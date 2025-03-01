from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info", views.ProductInfoApiView.as_view()),
    path("products/<int:pk>/", views.ProductDetailsAPIView.as_view()),
    path("orders/", views.OrderListAPIView.as_view()),
    path("user-orders/", views.UserOrderListAPIView.as_view(),name="user-orders"),
]
