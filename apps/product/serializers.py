from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields="__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        exclude=["active","added_on","stock"]