from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication import api


urlpatterns = [
    path('login/', api.LoginAPIView.as_view(), name='login'),
    path('logout/', api.LogoutAPIView.as_view(), name='logout'),
    path('register/', api.RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list_user/', api.ListUserAPIView.as_view(), name='list_user'),
]