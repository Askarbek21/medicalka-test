from rest_framework import serializers 

from .models import User 


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'full_name',
            'is_verified',
            'verification_token'
        ]


class UserChangeProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        min_length=3,
        max_length=32,
    )
    full_name = serializers.CharField(
        min_length=2,
        max_length=100,
    )


class UserChangeCredentialsSerializer(serializers.Serializer):
    password = serializers.CharField()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
        ]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=32)
    full_name = serializers.CharField(min_length=2, max_length=100)
    password = serializers.CharField()


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()