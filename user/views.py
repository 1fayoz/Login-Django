from .serializer import UserSerializer, VerifySerializer, LoginSerializer
from .models import User
from rest_framework.views import APIView
import random
from datetime import datetime,timedelta
from rest_framework.views import Response
from rest_framework.serializers import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class UserRegister(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')
        if User.objects.filter(phone=phone, status='approved').exists():
            raise ValidationError(
                detail={"error": "Bunday foydalanuvchi ro'yxatdan o'tgan"},
                code=400
            )
        
        user = User.objects.filter(phone=phone)
        if user.exists():
            user = user.first()
        else:
            user = User.objects.create(phone=phone)
        user.set_password(password)
        code = random.randrange(1000, 9999)      #''.join[str(random.randint(1,9) for i in range(4) )]
        user.code = code
        user.expire_date = datetime.now() + timedelta(seconds=60)
        user.save()

        print(code)
        return Response(
            data={
                "user": user.id
            },
            status=201
            )
    
class VerifyAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        code = serializer.validated_data.get('code')

        if timezone.now() > user.expire_date or code != user.code:
            raise ValidationError(detail={
                "error":"voqt otib ketti yoki code xato"},
                status = 400
                )
        user.status = "approved"
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={
                'token':token.key,
                'user':user.id
            }
        )
    

class UserLogin(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        phone = request.data.get('phone')
        password = request.data.get('password')

        user = authenticate(phone=phone, password=password)

        if user is None or user.status != "approved":
            raise ValidationError(detail={
                "error":"Siz ro'yxatdan o'tmagansiz"},
                code = 400
                )


        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={
                'token': token.key,
                'user': user.id
            }
        )