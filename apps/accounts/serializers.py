from .models import *
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

