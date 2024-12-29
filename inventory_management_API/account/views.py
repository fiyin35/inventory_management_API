from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        """This method tries to fetch the 
        Token associated with the specified user. 
        If it does not exist, it creates a new 
        Token for the user"""
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user': UserSerializer(user).data, 'created': created})

