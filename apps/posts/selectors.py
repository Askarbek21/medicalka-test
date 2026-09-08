from apps.auth.models import User

from .models import Post, Comment
from .exceptions import PostNotFound, CommentNotFound


def post_list() -> list[Post]:
    return Post.objects.select_related('author')


def post_get(post_id: int) -> Post:
    try:
        return Post.objects.select_related(
            'author'
            ).prefetch_related(
            'comments', 'likes', 'comments__author'
            ).get(id=post_id)
    except Post.DoesNotExist:
        raise PostNotFound()


def comment_get(comment_id: int) -> Comment:
    try:
        return Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise CommentNotFound()


def post_feed() -> list[User]:
    return User.objects.prefetch_related(
        'posts', 'posts__likes'
    ).all()