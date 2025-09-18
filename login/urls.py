from django.urls import path
from .api import CustomTokenObtainPairView,CustomTokenRefreshObtainPairView, login_admin

urlpatterns = [
    path('login-admin/', login_admin, name='login_admin'),
    path('access-token/', CustomTokenObtainPairView.as_view(), name='get_access_token'),
    path('refresh-token/', CustomTokenRefreshObtainPairView.as_view(), name='refresh_access_token'),
]