import datetime

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.core.cache import caches
import logging


from api.models import Product
from api.serializers import ProductSerializer


logger = logging.getLogger("api")


@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class ProductViewSet(ModelViewSet):
    """
    Products Resource.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        """
        GetAll

        Retrieve list all products
        """
        start = datetime.datetime.now()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        elapsed_time = (datetime.datetime.now() - start).total_seconds()
        logger.info(f"({elapsed_time:9}) List Products")
        return response

    def retrieve(self, request, *args, **kwargs):
        """
        GetbyId

        Retrieve product data py Id

        :param id:
        """
        start = datetime.datetime.now()
        instance = self.get_object()
        instance.status = caches['statuses'].get_or_set(instance.id, instance.status)
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        elapsed_time = (datetime.datetime.now() - start).total_seconds()
        logger.info(f"({elapsed_time:9}) Retrieve product id:{instance.id}")
        return response

    def create(self, request, *args, **kwargs):
        """
        Insert

        Create new Product
        """
        start = datetime.datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elapsed_time = (datetime.datetime.now() - start).total_seconds()
        logger.info(f"({elapsed_time:9}) Create new product")
        return response

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update

        Update Product by Id
        """
        start = datetime.datetime.now()
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elapsed_time = (datetime.datetime.now() - start).total_seconds()
        logger.info(f"({elapsed_time:9}) Update product id:{instance.id}")
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete

        Delete Product by Id
        """
        start = datetime.datetime.now()
        instance = self.get_object()
        response = super(ProductViewSet, self).destroy(request, pk, *args, **kwargs)
        elapsed_time = (datetime.datetime.now() - start).total_seconds()
        logger.info(f"({elapsed_time:9}) Retrieve product id:{instance.id}")
        return response