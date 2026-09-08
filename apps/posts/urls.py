from django.urls import path 

from .views import *


urlpatterns = [
    path('list', PostListApi.as_view(), name='post-list'),
    path('<uuid:post_id>', PostGetApi.as_view(), name='post-get'),
    path('create/', PostCreateApi.as_view(), name='post-create'),
    path('<uuid:post_id>/update/', PostUpdateApi.as_view(), name='post-update'),
    path('<uuid:post_id>/delete/', PostDeleteApi.as_view(), name='post-delete'),
    path('<uuid:post_id>/comments/create/', CommentCreateApi.as_view(), name='comment-create'),
    path('<uuid:post_id>/comments/<uuid:comment_id>/delete/', CommentDeleteApi.as_view(), name='comment-delete'),
    path('<uuid:post_id>/like/', PostLikeApi.as_view(), name='post-like'),
    path('<uuid:post_id>/unlike/', PostUnlikeApi.as_view(), name='post-unlike'),
]