from django.db import models

# Create your models here.

class ShipRocketToken(models.Model):
    token=models.CharField(max_length=250)
    added_on=models.DateTimeField(auto_now_add=True)
    def has_add_permission(self):
        return not ShipRocketToken.objects.exists()

