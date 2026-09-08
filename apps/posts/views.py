import uuid

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, GenericAPIView
)

from drf_spectacular.utils import extend_schema, inline_serializer

from apps.core.responses import success_response
from apps.core.utils import success_schema
from apps.core.constants import Tags
from apps.core.permissions import IsOwner, IsVerified

from .filters import PostFilter
from .serializers import *
from .services import *
from .selectors import *


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Получение списка постов',
    responses={
        200: success_schema(PostListSerializer, many=True),
    }
)
class PostListApi(ListAPIView):
    serializer_class = PostListSerializer
    filterset_class = PostFilter

    def get_queryset(self):
        return post_list()


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Получение информации о конкретном посте',
    responses={
        200: success_schema(PostGetSerializer),
    }
)
class PostGetApi(RetrieveAPIView):
    serializer_class = PostGetSerializer

    def get_queryset(self):
        return post_list()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data)


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Создание нового поста',
    responses={
        201: success_schema(PostGetSerializer),
    }
)
class PostCreateApi(GenericAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsVerified]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_post = post_create(
            title=serializer.validated_data.get('title'),
            content=serializer.validated_data.get('content'),
            author=request.user
        )

        return success_response(data=PostGetSerializer(new_post).data, status=201)


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Обновление информации о конкретном посте',
    responses={
        200: success_schema(PostGetSerializer),
    }
)
class PostUpdateApi(GenericAPIView):
    permission_classes = [IsOwner]
    serializer_class = PostUpdateSerializer

    def patch(self, request, post_id: uuid.UUID):

        post = post_get(post_id)
        self.check_object_permissions(request, post)
        
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_post = post_update(post=post, data=serializer.validated_data)
        
        return success_response(data=PostGetSerializer(updated_post).data)


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Удаление конкретного поста',
    responses={
        204: None,
    }
)
class PostDeleteApi(GenericAPIView):
    permission_classes = [IsOwner]

    def delete(self, request, post_id: uuid.UUID):

        post = post_get(post_id)
        self.check_object_permissions(request, post)

        post_delete(post)

        return success_response(status=204)


@extend_schema(
    tags=[Tags.COMMENTS], 
    summary='Создание нового комментария к посту',
    responses={
        201: success_schema(CommentListSerializer),
    }
)
class CommentCreateApi(GenericAPIView):
    permission_classes = [IsVerified]
    serializer_class = CommentCreateSerializer

    def post(self, request, post_id: uuid.UUID):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_comment = comment_create(
            post_id=post_id,
            content=serializer.validated_data.get('content'),
            author=request.user
        )

        return success_response(data=CommentListSerializer(new_comment).data, status=201)


@extend_schema(
    tags=[Tags.COMMENTS], 
    summary='Удаление конкретного комментария',
    responses={
        204: None,
    }
)
class CommentDeleteApi(GenericAPIView):
    permission_classes = [IsOwner]

    def delete(self, request, post_id: uuid.UUID, comment_id: uuid.UUID):

        comment = comment_get(comment_id)
        self.check_object_permissions(request, comment)

        comment_delete(comment)

        return success_response(status=204)


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Лайк конкретного поста',
    responses={
        200: inline_serializer(
            name='PostLikeResponse',
            fields={
                'message': serializers.CharField()
            }
        ),
    }
)
class PostLikeApi(GenericAPIView):

    def post(self, request, post_id: uuid.UUID):

        post = post_get(post_id)

        post_like(post=post, user=request.user)

        return success_response(data={'message': 'Пост успешно залайкан.'}, status=200)


@extend_schema(
    tags=[Tags.POSTS], 
    summary='Разлайк конкретного поста',
    responses={
        200: inline_serializer(
            name='PostUnlikeResponse',
            fields={
                'message': serializers.CharField()
            }
        ),
    }
)
class PostUnlikeApi(GenericAPIView):

    def delete(self, request, post_id: uuid.UUID):

        post = post_get(post_id)

        post_unlike(post=post, user=request.user)

        return success_response(data={'message': 'Пост успешно разлайкан.'}, status=200)
    

@extend_schema(
    tags=[Tags.POSTS], 
    summary='Получение ленты постов',
    responses={
        200: success_schema(UserFeedSerializer, many=True),
    }
)
class PostFeedApi(ListAPIView):
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        return post_feed()