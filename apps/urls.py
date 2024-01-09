from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.viewsets import ProductViewSet

router = DefaultRouter()
router.register(r"scan", ProductViewSet, basename="scan")

urlpatterns = [
    path("", include(router.urls)),
]
