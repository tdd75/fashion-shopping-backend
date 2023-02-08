from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('oauth-google/', OauthGoogleAPIView.as_view(), name='oauth_google'),
    path('oauth-facebook/', OauthFacebookAPIView.as_view(), name='oauth_facebook'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('recover-password/', RecoverPasswordView.as_view(),
         name='recover_password'),
    # admin routes
    path('admin/login/', AdminLoginAPIView.as_view(), name='admin_login'),
]
