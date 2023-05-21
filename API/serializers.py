from rest_framework import serializers
from . import models


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = [
            'id',
            'spu_id',
            'override_title',
            'override_brand',
            'create_time'
        ]
        read_only_fields = [
            'create_time'
        ]
