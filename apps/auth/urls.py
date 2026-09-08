from django.urls import path 

from .views import * 


urlpatterns = [
    path('login/', LoginApi.as_view(), name='user-login'),
    path('login/refresh/', LoginRefreshApi.as_view(), name='user-login-refresh'),
    path('verify-email', UserVerifyEmailApi.as_view(), name='user-verify-email'),
    path('verify-email/resend/', UserResendVerificationTokenApi.as_view(), name='user-resend-verification-token'),
    path('me', UserMeApi.as_view(), name='user-me'),
    path('register/', UserRegisterApi.as_view(), name='user-register'),
    path('change-profile/', UserChangeProfileApi.as_view(), name='user-change-profile'),
    path('change-credentials/', UserChangeCredentialsApi.as_view(), name='user-change-credentials'),
]