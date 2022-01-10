from ctypes import pythonapi
from hashlib import pbkdf2_hmac
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from MedMarket.MedMarket.settings import REST_FRAMEWORK

from .serializers import *
from .models import *
from .permissions import *
from .otp import OtpView






# Create your views here.

class LoginView(APIView):

    def get(self,request):
        data=request.GET
        phonenumber=data.get("phonenumber")
        try:
            user=User.objects.get(phonenumber=phonenumber)
        except:
            return Response({"error":"Phonenumber Not Found !!"},400)
        otp=OtpView().get_otp(phonenumber,user.email)
        return Response({"message":"otp sent succesfully!!"},200)

    def post(self, request):

        if request.user.is_authenticated:
            return Response({"error":"User already logged in."},400)

        phonenumber = request.data.get('phonenumber')
        password = request.data.get('password')

        if not phonenumber: return Response({"error":"phonenumber field missing"},400)
        if not password: return Response({"error":"Password field missing"},400)

        try:
            user_obj = User.objects.get(phonenumber=phonenumber)
        except:
            return Response({"error":"User doesn't exist with this phonenumber !!"},400)

        if user_obj.active:
            if user_obj.check_password(password):
                refresh = RefreshToken.for_user(user_obj)
                return Response({
                                'message':"success",
			                    'refresh': str(refresh),
			                    'access': str(refresh.access_token),
			                    'data': UserSerializer(instance=user_obj).data,
                				},200)
            else:
                return Response({'error':"Invalid password"},400)
        else:
            return Response({"error":"user doesn't verified the phonenumber !!",'user': UserSerializer(instance=user_obj).data},200)
    
    def put(self,request):
        data=request.data
        phonenumber=data.get("phonenumber")
        otp=data.get("otp")
        try:
            user=User.objects.get(phonenumber=phonenumber)
        except:
            return Response({"error":"Phonenumber Not Found !!"},400)
        if not otp: return Response({"error":"Please enter otp !"},422)
        temp=OtpView().validate_otp(otp,phonenumber,user.email)
        if(temp):
            refresh = RefreshToken.for_user(user)
            return Response({
                            'message':"success",
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'data': UserSerializer(instance=user).data,
                            },200)
        else:
            return Response({"error":"Otp is Invalid !!"},400)


    



class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get("refresh")
        if token is None:
            return Response({"error":"Refresh token not provided"},400)
        try:
            rtkn=RefreshToken(token)
            rtkn.blacklist()
        except:
            return Response({"error":"Unknown error occured."},400)
        return Response({"error":"Successfully logged out."},200)



class SignupView(APIView):

    def validate(self,request):
        data=request.data
        serializer=UserSerializer(data=data)
        if(serializer.is_valid()):
            password=data.get("password")
            if not password: return Response({"error":"Please Enter the Password ."},422)
            if not 5<=len(password)<=100: return Response({"error":"Password Length Should be atleast 5."},422)
        else:
            return Response({"error":serializer.errors},422)
    def get(self,request):
        return Response({"message":"success"},200)
    
    def post(self,request):
        check=self.validate(request)
        if check: 
            return check
        phonenumber=request.data.get("phonenumber")
        email=request.data.get("email")
        otp=OtpView().get_otp(phonenumber,email)
        return Response({"message":"success"},200)
    
    def put(self,request):
        check=self.validate(request)
        if check:
            return check
        serializer=UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error":serializer.errors},422)
        full_name=serializer.validated_data.get("full_name")
        phonenumber=serializer.validated_data.get("phonenumber")
        email=serializer.validated_data.get("email")
        password=request.data.get("password")
        otp=request.data.get("otp")
        if not otp: return Response({"error":"Please Enter The Otp !!"},422)
        temp=OtpView().validate_otp(otp,phonenumber,email)
        if(temp):
            user=User.objects.create_user(full_name=full_name,phonenumber=phonenumber,email=email,password=password)
            return Response({"message":"User Account Created SuccessFully !"},200)
        else:
            return Response({"error":"Invalid OTP !"},400)



class ForgotPasswordView(APIView):

    def get(self,request):
        data=request.GET
        phonenumber=data.get("phonenumber")
        try:
            user=User.objects.get(phonenumber=phonenumber)
        except:
            return Response({"error":"Phonenumber Not Found !!"},400)
        otp=OtpView().get_otp(phonenumber,user.email)
        return Response({"message":"otp sent succesfully!!"},200)
    
    def post(self,request):
        data=request.data
        phonenumber=data.get("phonenumber")
        password=data.get("password")
        otp=data.get("otp")
        try:
            user=User.objects.get(phonenumber=phonenumber)
        except:
            return Response({"error":"Phonenumber Not Found !!"},400)
        if not otp: return Response({"error":"Please enter otp !"},422)
        if not password: return Response({"error":"Please enter password !"},422)
        temp=OtpView().validate_otp(otp,phonenumber,user.email)
        if temp:
            user.set_password(password)
            user.save()
            return Response({"message":"password set successfully"},200)
        else:
            return Response({"error":"invalid otp !!"},400)






       




