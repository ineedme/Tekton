from rest_framework import serializers
from django.core.cache import caches
import random
import requests

from api.models import Product, Status



class ProductSerializer(serializers.ModelSerializer):
    """

    """
    status = serializers.IntegerField(source='status.key', read_only=False)
    discount = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'status', 'stock', 'description', 'price', 'discount', 'final_price', 'created_at', 'updated_at')
        read_only_fields = ('id', )

    def __fetch_discount__(self, id):
        headers = {
            "X-API-Key": "7a867240"
        }
        url = f"https://my.api.mockaroo.com/discount/{id}.json"
        responde = requests.get(url, headers=headers)
        return responde.json().get('discount', random.randint(0, 100))

    def get_discount(self, obj):
        #print("get discount")
        discount = caches['default'].get_or_set(obj.id, self.__fetch_discount__(obj.id))
        return discount

    def get_final_price(self, obj):
        return obj.price * (100 - self.get_discount(obj)) / 100

    def create(self, validated_data):
        """
        Create Product

        :param validated_data:
        :return:
        """
        validated_data["status"] = Status.objects.get(key=validated_data["status"]["key"])
        instance = Product.objects.create(**validated_data)
        caches['statuses'].set(instance.id, instance.status)
        return instance

    def update(self, instance, validated_data):
        validated_data["status"] = Status.objects.get(key=validated_data["status"]["key"])
        caches['statuses'].set(instance.id, validated_data["status"])
        instance = super(ProductSerializer, self).update(instance, validated_data)
        return instance
