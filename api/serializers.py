from rest_framework import serializers
from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'status', 'stock', 'description', 'price', 'created_at', 'updated_at')
