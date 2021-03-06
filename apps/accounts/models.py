from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
import uuid

# Create your models here.

class User(AbstractBaseUser):
	id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	full_name=models.CharField(max_length=255)
	email=models.EmailField(unique=True,max_length=255)
	phonenumber=models.CharField(max_length=255,unique=True)
	email_verify=models.BooleanField(default=False)
	admin=models.BooleanField(default=False)
	staff=models.BooleanField(default=False)
	active=models.BooleanField(default=False)
	date_joined=models.DateTimeField(auto_now_add=True)
	verified=models.BooleanField(default=False)
	status=models.CharField(max_length=250,default="OnHold")#Approved,Suspended
	credit=models.DecimalField(max_digits=10,decimal_places=2,default=0)

	USERNAME_FIELD='phonenumber'

	REQUIRED_FIELDS=['full_name','email']

	objects=MyUserManager()

	def __str__(self):
		return str(self.phonenumber)
	

	def save(self,*args,**kwargs):
		if(self.status=="Approved"):
			self.verified=True
		else:
			self.verified=False
		super().save(*args,**kwargs)
	
	@property
	def is_active(self):
		return self.active

	@property
	def is_admin(self):
		return self.admin
	
	@property
	def is_staff(self):
		return self.staff
	
	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
	    return True

    




