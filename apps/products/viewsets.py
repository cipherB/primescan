from django.db import transaction
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.serializers import inline_serializer
from apps.mixins import CustomResponseMixin
import logging
from .services import ProductService

logger = logging.getLogger("django.request")

class ProductViewSet(CustomResponseMixin, viewsets.ViewSet):
    @action(
        detail=False,
        methods=["post"],
        url_path="scan-code",
        permission_classes=[AllowAny],
    )
    def scan_code(self, request):
        serialized_data = inline_serializer(
            fields={
                "image": serializers.FileField(),
            },
            data=request.data,
        )
        errors = self.validate_serializer(serialized_data)
        if errors:
            logger.info("Request received: %s", request)
            return errors

        response = ProductService().scan_code(request, **serialized_data.validated_data)
        logger.info("Request received: %s", request)
        return self.response(response)
    
    @action(
        detail=False,
        methods=["get"],
        url_path="fetch-products",
        permission_classes=[AllowAny],
    )
    @transaction.atomic
    def fetch_products(self, request):
        response = ProductService().fetch_products(request=request)
        logger.info("Request received: %s", request)
        return self.response(response)