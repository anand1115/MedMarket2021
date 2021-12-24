from .models import *
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    def validate_full_name(self,full_name):
        if(not 3<len(full_name)<100):
            raise serializers.ValidationError("Invalid Full Name.")
        return full_name
    
    def validate_phonenumber(self,phonenumber):
        if(not phonenumber.isdigit() or len(phonenumber)!=10):
            raise serializers.ValidationError("Invalid Phone Number.")
        return phonenumber
        
    def validate_email(self,email):
        if not 3<=len(email)<=50:
            raise serializers.ValidationError("Invalid email !")
        return email



