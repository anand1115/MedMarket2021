from .models import *
from apps.product.models import Product

class MyCart:

    def __init__(self,request):
        self.user=request.user
        self.cart=self.getcart()
        self.promocode=self.cart.promocode
        self.address=self.cart.address
    
    def getcart(self):
        try:
            cart,created=Cart.objects.get_or_create(user=self.user,status=False)
        except:
            Cart.objects.filter(user=self.user,status=False).delete()
            cart,created=Cart.objects.get_or_create(user=self.user,status=False)
        return cart
    
    def getcartitems(self):
        items=CartItem.objects.filter(cart=self.cart)
        return items
    
    def add(self,product,count=1):
        item,created=CartItem.objects.get_or_create(product=product,cart=self.cart)
        quantity=item.quantity
        if(quantity+count > item.product.stock):
            raise Exception("Product Is Out Of Stock !!")
        item.quantity+=count
        item.save()
    
    def remove(self,product,count=1):
        item,created=CartItem.objects.get_or_create(product=product,cart=self.cart)
        quantity=item.quantity
        if(quantity-count <= 0):
            item.delete()
            return
        item.quantity-=count
        item.save()
    
    def clear(self,product):
        try:
            item=CartItem.objects.get(product=product,cart=self.cart)
            item.delete()
        except:
            pass
    
    def get_items(self):
        return CartItem.objects.filter(cart=self.cart)

    def check_promocode(self,promocode):
        for i in self.get_items():
            categories=set(promocode.category.all())
            product_category=set(i.product.category.all())
            if(categories & product_category):
                return True
            subcategories=set(promocode.subcategory.all())
            product_subcategory=set(i.product.subcategory.all())
            if(subcategories & product_subcategory):
                return True
            if i.product in list(promocode.product.all()):
                return True
            return False
    
    def apply_promocode(self,promocode):
        if(self.check_promocode(promocode)):
            if(self.cart.total_selling_price<promocode.minimum_order_value):
                return False
            cart=self.cart
            cart.promocode=promocode
            cart.save()
            return True
    
    def set_address(self,address):
        cart=self.cart
        cart.address=address
        cart.save()


import requests
import json
from apps.mainadmin.models import ShipRocketToken

class ShipRocket:
    def __init__(self,cart):
        self.cart=cart
        self.address=self.cart.address
    
    def check_serivce(self):
        if(not self.address):
            return False
        url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {{token}}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        
    

        

    
    

    

    

