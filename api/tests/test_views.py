import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import caches

from api.models import Product, Status
from api.serializers import ProductSerializer

client = Client()

class GetAllProductsTest(TestCase):
    """ Test module for GET all Products API """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        # ('name', 'status', 'stock', 'description', 'price'
        Product.objects.create(
            name='iphone', status_id=1, stock=1, description='iphone', price=5.0
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

    def test_products_empty(self):
        # delete products data
        Product.objects.all().delete()
        response = client.get(reverse('product-list'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewProductTest(TestCase):
    """ Test module for inserting a new product """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        self.valid_payload = {
            'name': 'iphone',
            'status': 1,
            'stock': 1,
            'description': 'iphone',
            'price': 5.0,
        }
        self.invalid_payload = {
            'name': '',
            'status_id': 1,
            'stock': 1,
            'description': 'Delicious',
            'price': 5.0,
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('product-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSingleProductTest(TestCase):
    """ Test GET single product API """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        # ('name', 'status', 'stock', 'description', 'price'
        self.product1 = Product.objects.create(
            name='iphone', status_id=1, stock=1, description='iphone', price=5.0
        )
        self.product2 = Product.objects.create(
            name='Fried Fish', status_id=1, stock=2, description='Yummy', price=4.0
        )

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('product-detail', kwargs={'pk': self.product1.pk}))
        product = Product.objects.get(pk=self.product1.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('product-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleProductTest(TestCase):
    """ Test updating an existing product record """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        self.product1 = Product.objects.create(
            name='iphone', status_id=1, stock=1, description='iphone', price=5.0
        )
        self.product2 = Product.objects.create(
            name='Fried Fish', status_id=1, stock=2, description='Yummy', price=4.0
        )
        self.valid_payload = {
            'name': 'iphone',
            'status': 1,
            'stock': 1,
            'description': 'iphone',
            'price': 5.0,
        }
        self.invalid_payload = {
            'name': '',
            'status_id': 1,
            'stock': 1,
            'description': 'Delicious',
            'price': 5.0,
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('product-detail', kwargs={'pk': self.product1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_update_product(self):
        response = client.put(
            reverse('product-detail', kwargs={'pk': self.product2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_no_existing_product(self):
        response = client.put(
            reverse('product-detail', kwargs={'pk': 30}),
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleProductTest(TestCase):
    """ Test deleting an existing product record """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        self.product1 = Product.objects.create(
            name='iphone', status_id=1, stock=1, description='iphone', price=5.0
        )

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('product-detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('product-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class StoreProductStatusCacheTest(TestCase):
    """ Test Store Product Status in Cache """

    def setUp(self):
        Status.objects.create(key=1, name="Active")
        self.valid_payload = {
            'name': 'iphone',
            'status': 1,
            'stock': 1,
            'description': 'iphone',
            'price': 5.0,
        }

    def test_store_product_status_on_create(self):
        response = client.post(
            reverse('product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        dict = response.json()
        self.assertEqual(dict["status"], caches["statuses"].get(dict["id"]).id)

    def test_product_status_validation_on_update(self):
        valid_payload = self.valid_payload.copy()
        valid_payload["status"] = Status.objects.get(key=1)
        product1 = Product.objects.create(**valid_payload)
        response = client.put(
            reverse('product-detail', kwargs={'pk': product1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        dict = response.json()
        self.assertEqual(dict["status"], caches["statuses"].get(dict["id"]).id)