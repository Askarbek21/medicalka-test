from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, inline_serializer

from apps.auth.services import delete_expired_unverified_users
from apps.posts.services import delete_expired_posts

from .responses import success_response
from .models import SiteConfig
from .constants import Tags
from .serializers import *


@extend_schema(tags=[Tags.SETTINGS], summary='Получение и обновление настроек сайта')
class SiteConfigApi(RetrieveUpdateAPIView):
    serializer_class = SiteConfigSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return SiteConfig.load()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)


@extend_schema(
    tags=[Tags.SETTINGS], 
    summary='Удаление просроченных постов',
    responses={
        200: inline_serializer(
            name='DeleteExpiredPostsResponse',
            fields={
                'deleted_posts_count': serializers.IntegerField(),
            }
        )
    }
)
class DeleteExpiredPostsApi(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request):
        deleted_count = delete_expired_posts()
        return success_response(data=deleted_count)


@extend_schema(
    tags=[Tags.SETTINGS], 
    summary='Удаление просроченных неподтвержденных пользователей',
    responses={
        200: inline_serializer(
            name='DeleteExpiredUnverifiedUsersResponse',
            fields={
                'deleted_users_count': serializers.IntegerField(),
            }
        )
    }
)
class DeleteExpiredUnverifiedUsersApi(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request):
        deleted_count = delete_expired_unverified_users()
        return success_response(data=deleted_count)