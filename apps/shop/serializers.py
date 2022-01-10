from .models import *
from rest_framework import serializers
from apps.product.serializers import *
from apps.accounts.serializers import *

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Promocode
        fields="__all__"
    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['category']=CategorySerializer(instance.category.all(),many=True).data
        data['product']=ProductSerializer(instance.product.all(),many=True).data
        data['subcategory']=ProductSerializer(instance.subcategory.all(),many=True).data
        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"
    
    def validate_pincode(self,value):
        if ((not value.isdigit()) or (len(value)!=6)):
            raise serializers.ValidationError("Please Give Valid Pincode !!")
        return value
    
    def validate_phonenumber(self,value):
        if ((not value.isdigit()) or (len(value)!=10)):
            raise serializers.ValidationError("Please Give Valid Phonenumber !!")
        return value
    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['user']=UserSerializer(instance.user).data
        return data



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        exclude=["cart"]
    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data["total_item_selling_price"]=instance.item_selling_price
        data["total_item_marked_price"]=instance.item_marked_price
        data["total_item_discount_price"]=instance.item_discount_price
        data['product']=ProductSerializer(instance.product).data
        data["cart"]=str(instance.cart.id)
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"
    
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data["total_selling_price"]=instance.total_selling_price
        data["total_marked_price"]=instance.total_marked_price
        data["total_discount_price"]=instance.total_discount_price
        data["total_promocode_discount_price"]=instance.total_promocode_discount_price
        data["cart_items"]=CartItemSerializer(CartItem.objects.filter(cart=instance),many=True).data
        data["promocode"]=PromoCodeSerializer(instance.promocode).data if instance.promocode else None
        data["address"]=AddressSerializer(instance.address).data if instance.address else None
        data["user"]=UserSerializer(instance.user).data
        return data
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"



