from datetime import timedelta

from django.utils import timezone

from apps.auth.models import User

from apps.core.models import SiteConfig

from .models import Post, Comment, Like 
from .exceptions import PostAlreadyLiked, PostCannotBeLiked


def post_create(title: str, content: str, author: User) -> Post:

    new_post = Post(title=title, content=content, author=author)

    new_post.full_clean()
    new_post.save()

    return new_post


def post_update(post: Post, data: dict) -> Post:
    
    for attr, value in data.items():
        setattr(post, attr, value)

    post.full_clean()
    post.save()

    return post


def post_delete(post: Post) -> None:
    post.delete()


def comment_create(
        post: Post, 
        content: str, 
        author: User
    ) -> Comment:

    new_comment = Comment(post=post, content=content, author=author)

    new_comment.full_clean()
    new_comment.save()

    return new_comment


def comment_delete(comment: Comment) -> None:

    comment.delete()


def post_like(user: User, post: Post) -> Like:

    if post.author.id == user.id:
        raise PostCannotBeLiked()

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        raise PostAlreadyLiked()

    return like


def post_unlike(post: Post, user: User) -> None:

    if post.author.id == user.id:
        raise PostCannotBeLiked()

    like = Like.objects.filter(user=user, post=post).first()

    if like:
        like.delete()


def delete_expired_posts() -> dict:
    settings_obj = SiteConfig.load()

    deadline = timezone.now() - timedelta(
        days=settings_obj.post_ttl_days
    )

    deleted_count, _ = Post.objects.filter(
        created_at__lt=deadline
    ).delete()

    return {
        'deleted_posts_count': deleted_count,
    }