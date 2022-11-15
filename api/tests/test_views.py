import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from api.models import Product, Status
from api.serializers import ProductSerializer

client = Client()

class GetAllPuppiesTest(TestCase):
    """ Test module for GET all Products API """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        # ('name', 'status', 'stock', 'description', 'price'
        Product.objects.create(
            name='Fried Chicken', status_id=1, stock=1, description='Delicious', price=5.0
        )
        Product.objects.create(
            name='Fried Fish', status_id=1, stock=2, description='Yummy', price=4.0
        )

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('product-list'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
