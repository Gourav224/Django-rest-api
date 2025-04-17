from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info", views.ProductInfoApiView.as_view()),
    path("products/<int:pk>/", views.ProductDetailsAPIView.as_view()),
]


router = DefaultRouter()

router.register("orders", views.OrderViewSet)

urlpatterns += router.urls
