from . import models
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.User
#         fields = (
#             'phone',
#             'password',
#         )

class UserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class VerifySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset= models.User.objects.filter(status="new"))
    code = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = (
            'phone',
            'password',
        )
