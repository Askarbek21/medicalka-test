from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from drf_spectacular.utils import extend_schema, inline_serializer

from apps.core.responses import success_response
from apps.core.constants import Tags
from apps.core.utils import success_schema

from .serializers import *
from .services import *
from .throttlers import LoginRateThrottle


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Получение access и refresh токенов для авторизации пользователя',
    responses={
        200: success_schema(TokenObtainPairSerializer),
    }
)
class LoginApi(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Обновление access токена по refresh токену',
    responses={
        200: success_schema(TokenRefreshSerializer),
    }
)
class LoginRefreshApi(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Получение информации о текущем пользователе',
    responses={
        200: success_schema(UserMeSerializer),
    }
)
class UserMeApi(GenericAPIView):
    serializer_class = UserMeSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)

        return success_response(data=serializer.data)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Регистрация нового пользователя',
    responses={
        201: success_schema(UserMeSerializer),
    }
)
class UserRegisterApi(GenericAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = user_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
            full_name=serializer.validated_data.get('full_name'),
            password=request.data.get('password')
        )

        return success_response(data=UserMeSerializer(new_user).data, status=201)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Изменение профиля текущего пользователя',
    responses={
        200: success_schema(UserMeSerializer),
    }
)
class UserChangeProfileApi(GenericAPIView):
    serializer_class = UserChangeProfileSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = user_change_profile(
            user=request.user,
            data=serializer.validated_data
        )

        return success_response(data=UserMeSerializer(user).data)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Изменение учетных данных текущего пользователя',
    responses={
        200: success_schema(UserMeSerializer),
    }
)
class UserChangeCredentialsApi(GenericAPIView):
    serializer_class = UserChangeCredentialsSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_change_credentials(
            user=request.user,
            password=serializer.validated_data.get('password')
        )

        return success_response(data=UserMeSerializer(user).data)


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Подтверждение email пользователя',
    responses={
        200: inline_serializer(
            name='UserVerifyEmailResponse',
            fields={'message': serializers.CharField(),}
        )
    }
)
class UserVerifyEmailApi(GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        verify_email_token(
            token=serializer.validated_data.get('token')
        )

        return success_response(data={'message': 'Email успешно подтвержден.'})


@extend_schema(
    tags=[Tags.AUTH], 
    summary='Повторная отправка токена подтверждения email',
    responses={
        200: inline_serializer(
            name='UserResendVerificationTokenResponse',
            fields={'message': serializers.CharField()}    
        )
    }
)
class UserResendVerificationTokenApi(GenericAPIView):

    def post(self, request):
        
        token = generate_verification_token(request.user)

        return success_response(data={'message': 'Новый токен подтверждения: {}'.format(token)})