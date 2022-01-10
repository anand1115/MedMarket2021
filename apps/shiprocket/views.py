from requests.api import head
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder  


from apps.accounts.permissions import *
from apps.shop.services import MyCart
from apps.mainadmin.models import ShipRocketToken

import requests
import json


class CheckCourier(APIView):
    permission_classes=[IsVerified]
    def get(self,request):
        mycart=MyCart(request)
        if not mycart.address:
            return Response({"error":"Please Add Address !!"},400)
        pickup_pincode=523211
        delivery_pincode=mycart.address.pincode
        token,_=ShipRocketToken.objects.get_or_create(active=True)
        url="https://apiv2.shiprocket.in/v1/external/courier/serviceability/"
        payload=json.dumps({"pickup_postcode":pickup_pincode,"delivery_postcode":delivery_pincode,"weight":mycart.cart.get_weight,"cod":0},cls=DjangoJSONEncoder)
        headers={'Content-Type': 'application/json','Authorization': 'Bearer {}'.format(token.token)}
        print(headers,payload)
        response=requests.request("GET",url,headers=headers,data=payload)
        if(response.status_code==200):
            data=response.json()
            status=data.get('status')
            if(status==200):
                return Response({"status":True,"data":data},200)
            else:
                return Response({"status":False,"data":data},400)
        else:
            return Response({"status":False,"error":response.json()},400)