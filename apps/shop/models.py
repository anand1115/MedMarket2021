from django.db import models
from django.db.models.base import Model
from apps.product.models import Product,Category,SubCategory
from apps.accounts.models import User
import uuid

from datetime import datetime
import pytz


class Promocode(models.Model):
    id=models.UUIDField(editable=False,primary_key=True,default=uuid.uuid4)
    code=models.CharField(max_length=250,unique=True)
    active=models.BooleanField(default=True)
    start=models.DateTimeField()
    end=models.DateTimeField()
    category=models.ManyToManyField(Category,blank=True)
    product=models.ManyToManyField(Product,blank=True)
    subcategory=models.ManyToManyField(SubCategory,blank=True)
    discount=models.PositiveSmallIntegerField()
    description=models.CharField(max_length=500)
    maximum_discount=models.DecimalField(decimal_places=2,max_digits=20)
    minimum_order_value=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    
    def save(self,*args,**kwargs):
        if(not 0<=self.discount<=100):
            self.discount=0
        now=datetime.now(pytz.timezone('Asia/Kolkata'))
        if(not self.start<=now<=self.end):
            self.active=False
        else:
            self.active=True
        super().save(*args,**kwargs)
	

class Address(models.Model):
	id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
	user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
	name=models.CharField(max_length=200)
	address=models.CharField(max_length=500,null=False)
	landmark=models.CharField(max_length=500,null=False)
	city=models.CharField(max_length=500,null=False)
	state=models.CharField(max_length=200,null=False)
	country=models.CharField(max_length=200,null=False)
	pincode=models.CharField(max_length=200,null=False)
	added_on=models.DateTimeField(auto_now_add=True)
	mobile=models.CharField(max_length=200)
	active=models.BooleanField(default=True)
    


class Cart(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    promocode=models.ForeignKey(Promocode,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    modified_on=models.DateTimeField(auto_now_add=True)
    prepaid=models.BooleanField(default=True)

    @property
    def total_selling_price(self):
        cartitems=self.cartitem_set.all()
        total_price=sum([i.item_selling_price for i in cartitems])-self.total_promocode_discount_price
        return round(total_price,2)

    @property
    def total_marked_price(self):
        cartitems=self.cartitem_set.all()
        total_price=sum([i.item_marked_price for i in cartitems])
        return round(total_price,2)
        
    @property
    def total_discount_price(self):
        cartitems=self.cartitem_set.all()
        total_price=sum([i.item_discount_price for i in cartitems])
        return round(total_price,2)
    
    @property
    def total_promocode_discount_price(self):
        cartitems=self.cartitem_set.all()
        total_price=sum([i.item_promocode_discount_price for i in cartitems])
        if(self.promocode):
            if(total_price>self.promocode.maximum_discount):
                total_price=self.promocode.maximum_discount
        return round(total_price,2)
    
    @property
    def get_weight(self):
        cartitems=self.cartitem_set.all()
        total_weight=sum([i.item_weight for i in cartitems])
        return round(total_weight,2)




class CartItem(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True)


    @property
    def item_selling_price(self):
        return self.product.selling_price*self.quantity
    
    @property
    def item_discount_price(self):
        return self.product.discount_price*self.quantity

    @property
    def item_marked_price(self):
        return self.product.marked_price*self.quantity
    
    @property
    def item_weight(self):
        return self.product.weight*self.quantity

    @property
    def item_promocode_discount_price(self):
        k=self.cart.promocode
        if(k and self.check_promocode and k.active):
            temp=((self.item_selling_price*k.discount)//100)
            return temp
        else:
            return 0

    @property
    def check_promocode(self):
        if(self.cart.promocode):
            categories=set(self.cart.promocode.category.all())
            product_category=set(self.product.category.all())
            if(categories & product_category):
                return True
            subcategories=set(self.cart.promocode.subcategory.all())
            product_subcategory=set(self.product.subcategory.all())
            if(subcategories & product_subcategory):
                return True
            if self.product in list(self.cart.promocode.product.all()):
                return True
            return False



class Order(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    details=models.JSONField(default=dict)
    added_on=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=250,default="ordered")
    prepaid=models.BooleanField()
    active=models.BooleanField(default=True)


class MCredit(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    paid=models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True)
    
    





