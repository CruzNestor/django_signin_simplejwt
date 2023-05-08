from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from authentication.serializers.auth_serializer import LoginSerializer, RegisterSerializer
from authentication.serializers.user_serializer import UserSerializer
from authentication.utils.create_jwt import get_tokens_for_user


class LoginAPIView(APIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        jwt = get_tokens_for_user(user)

        return Response(
            data=jwt,
            status=status.HTTP_200_OK
        )
        

class LogoutAPIView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try: 
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    
class RegisterAPIView(APIView):

    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        jwt = get_tokens_for_user(user)
        
        return Response(
            data=jwt,
            status=status.HTTP_201_CREATED
        )
        
        
class ListUserAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
            
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )