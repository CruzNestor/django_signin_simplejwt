from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.Serializer):
    
    class Meta():
        model = User
        fields = ['id', 'username', 'email']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'username': instance.username,
            'created_at': instance.created_at
        }