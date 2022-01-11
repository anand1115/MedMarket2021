from django.contrib.admin.decorators import action
from django.db import models

# Create your models here.

class ShipRocketToken(models.Model):
    token=models.CharField(max_length=500,default="token")
    added_on=models.DateTimeField(auto_now_add=True)
    # active=models.BooleanField(default=True,unique=True)
    
    def has_add_permission(self):
        return not ShipRocketToken.objects.exists()

