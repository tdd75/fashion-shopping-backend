from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairAPIView, OauthGoogleAPIView, RegisterAPIView

urlpatterns = [
    path('login/', MyObtainTokenPairAPIView.as_view(), name='token_obtain_pair'),
    path('oauth-google/', OauthGoogleAPIView.as_view(), name='oauth_google'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
