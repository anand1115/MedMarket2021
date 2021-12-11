from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import *
from .permissions import *






# Create your views here.

class LoginView(APIView):

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
			                    'refresh': str(refresh),
			                    'access': str(refresh.access_token),
			                    'data': UserSerializer(instance=user_obj).data,
                				},200)
            else:
                return Response({'error':"Invalid password"},400)
        else:
            return Response({"error":"user doesn't verified the phonenumber !!",'user': UserSerializer(instance=user_obj).data},200)



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



