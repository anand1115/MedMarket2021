from django.shortcuts import render
from django.utils.translation import activate
from rest_framework import response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.permissions import *

from .models import *
from .serializers import *

from .services import *


class CartView(APIView):
    permission_classes=[IsVerified]

    def get(self,request):
        mycart=MyCart(request)
        mycart.cart.address=None
        mycart.cart.promocode=None
        mycart.cart.save()
        data=CartSerializer(mycart.cart).data
        return Response({"message":"Success","data":data},200)
    
    def check(self,request):
        data=request.data
        product_id=data.get("product_id")
        count=data.get("count")
        try:
            count=int(count)
        except:
            return Response({"error":"invalid count"},400)
        try:
            product=Product.objects.get(id=product_id)
        except:
            return Response({"error":"Invalid Product Id"},400)
        if(count<=0):
            count=1
        return (product,count)

    
    def post(self,request):
        temp=self.check(request)
        if(isinstance(temp,tuple)):
            product,count=temp
        else:
            return temp
        mycart=MyCart(request)
        try:
            mycart.add(product,count)
        except:
            return Response({"message":"Product of stock !!"},202)
        return Response({"message":"product added to cart successfully !!"},200)
    

    def put(self,request):
        temp=self.check(request)
        if(isinstance(temp,tuple)):
            product,count=temp
        else:
            return temp
        mycart=MyCart(request)
        try:
            mycart.remove(product,count)
        except:
            return Response({"message":"Product of stock !!"},202)
        return Response({"message":"product removed from cart successfully !!"},200)
    
    def delete(self,request):
        data=request.GET
        product_id=data.get("product_id")
        try:
            product=Product.objects.get(id=product_id)
        except:
            return Response({"error":"Invalid Product Id"},400)
        mycart=MyCart(request)
        mycart.clear(product)
        return Response({"message":"product removed from cart succesfully!!"},200)


class PromoCodeView(APIView):
    permission_classes=[IsVerified]

    def get(self,request):
        now=datetime.now(pytz.timezone('Asia/Kolkata'))
        codes=Promocode.objects.filter(active=True,start__lt=now,end__gt=now)
        data=PromoCodeSerializer(codes,many=True).data
        return Response({"data":data},200)
    
    def post(self,request):
        mycart=MyCart(request)
        data=request.data
        promocode_id=data.get("promocode_id")
        try:
            promocode=Promocode.objects.get(id=promocode_id)
        except:
            return Response({"error":"Invalid Promocode"},400)
        if(not mycart.apply_promocode(promocode)):
            return Response({"message":"Promocode couldn't applied"},200)
        return Response({"message":"Promocode Applied Successfully"},200)


class AddressView(APIView):
    permission_classes=[IsVerified]

    def get(self,request):
        data=AddressSerializer(Address.objects.filter(user=request.user,active=True),many=True).data
        return Response({"message":"success","data":data},200)
    
    def post(self,request):
        data=request.data
        serializer=AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message":"Address Added successfully"},200)
        else:
            return Response({"error":serializer.errors},422)
    
    def put(self,request):
        data=request.data
        try:
            address=Address.objects.get(id=data.get("address_id"))
        except:
            return Response({"error":"Invalid Address id"},400)
        serializer=AddressSerializer(address,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Address updated successfully"},200)
        else:
            return Response({"error":serializer.errors},422)
    
    def delete(self,request):
        data=request.GET.get("address_id")
        try:
            address=Address.objects.get(id=data,active=True)
        except:
            return Response({"error":"Invalid Address Id"},400)
        address.active=False
        address.save()
        return Response({"message":"address deleted successfully !!"},200)




class CheckOutView(APIView):
    permission_classes=[IsVerified]

    def get(self,request):
        mycart=MyCart(request)
        data=CartSerializer(mycart.cart).data
        return Response({"message":"Success","data":data},200)
    
    def put(self,request):
        data=request.data
        try:
            address=Address.objects.get(id=data.get("address_id"))
        except:
            return Response({"error":"Invalid Address id"},400)
        mycart=MyCart(request)
        mycart.set_address(address)
        return Response({"message":"Address updated successfully"},200)
        
        
    

    



