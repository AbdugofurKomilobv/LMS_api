from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import LohinAPIView,LogoutView,CurrentUserView,CheckUserAuthenticationView


app_name = 'auth'

urlpatterns = [
    path('login/',LohinAPIView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('check/', CheckUserAuthenticationView.as_view(), name='check'),
   
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]