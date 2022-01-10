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
    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['category']=CategorySerializer(instance.category).data
        return data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        exclude=["active","added_on","stock"]

    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['category']=CategorySerializer(instance.category.all(),many=True).data
        data['subcategory']=SubCategorySerializer(instance.subcategory.all(),many=True).data
        return data