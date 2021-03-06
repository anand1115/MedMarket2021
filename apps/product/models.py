from typing import Match
from django.db import models
import uuid


def image_dict():
    return dict([("main",""),("other",[])])

class Category(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=250,unique=True)
    images=models.JSONField(default=image_dict)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=["title"]
    
    def __str__(self):
        return self.title

class SubCategory(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=250)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    images=models.JSONField(default=image_dict)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=["title"]
    
    def __str__(self):
        return self.title



class Brand(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=250,unique=True)
    images=models.JSONField(default=image_dict)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=["title"]
    
    def __str__(self):
        return self.title   



class Product(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=250,unique=True)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(SubCategory,blank=True)
    company=models.CharField(max_length=250)
    stock=models.IntegerField()
    active=models.BooleanField(default=True)
    quantity=models.IntegerField()
    quantity_type=models.CharField(max_length=250,null=True,blank=True)
    discount=models.PositiveSmallIntegerField(default=0)
    marked_price=models.DecimalField(decimal_places=2,max_digits=30)
    selling_price=models.DecimalField(decimal_places=2,max_digits=30)
    discount_price=models.DecimalField(decimal_places=2,max_digits=30,null=True,blank=True)
    images=models.JSONField(default=image_dict)
    description=models.TextField(null=True,blank=True)
    key_benifits=models.TextField(null=True,blank=True)
    direction_of_usage=models.TextField(null=True,blank=True)
    safety_information=models.TextField(null=True,blank=True)
    other_information=models.TextField(null=True,blank=True)
    added_on=models.DateTimeField(auto_now_add=True)
    expiry_date=models.DateField()
    batch_number=models.CharField(max_length=250)
    length=models.DecimalField(decimal_places=2,max_digits=50)
    breadth=models.DecimalField(decimal_places=2,max_digits=50)
    height=models.DecimalField(decimal_places=2,max_digits=50)
    weight=models.DecimalField(decimal_places=2,max_digits=50)

    def save(self,*args,**kwargs):
        if(self.selling_price>=self.marked_price):
            self.selling_price=self.marked_price
            self.discount_price=0
            self.discount=0
        else:
            self.discount_price=round((self.marked_price-self.selling_price),2)
            self.discount=100-((self.selling_price/self.marked_price)*100)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title+"({})".format(self.id)



    

