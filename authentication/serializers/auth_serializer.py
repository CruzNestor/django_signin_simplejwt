from django.db import Error
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from authentication.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        try:
            username_or_email = data['username'].lower().strip()
            user = User.objects.get(Q(email=username_or_email)|Q(username=username_or_email))

            if not user.check_password(data['password']):
                raise serializers.ValidationError('The password is incorrect.')
            
            if not user.is_active:
                raise serializers.ValidationError('The account is inactive.')
        
            return user
        
        except User.DoesNotExist:
            raise serializers.ValidationError('The user does not exist.')
        

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'username': {'required': True}
        }
    
    def create(self, validatedData):
        try:
            user = User.objects.create(
                email = validatedData['email'].lower().strip(),
                password = make_password(validatedData['password']),
                username = validatedData['username'].lower().strip()
            )
            return user
        except Error as e:
          raise serializers.ValidationError(e)
        