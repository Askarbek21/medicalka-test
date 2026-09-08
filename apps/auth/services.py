import uuid 

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.core.models import SiteConfig

from .models import User 
from .exceptions import *


def user_create(
    email: str, 
    username: str, 
    full_name: str, 
    password: str
    ) -> User:
    
    new_user = User(
        email=email,
        username=username,
        full_name=full_name
    )
    new_user.set_password(password)

    new_user.full_clean()
    new_user.save()

    generate_verification_token(new_user)

    return new_user


def user_change_profile(
    user: User, 
    data: dict
    ) -> User:
    
    for field, value in data.items():
        setattr(user, field, value)

    user.full_clean()
    user.save()

    return user


def user_change_credentials(
    user: User, 
    password: str
    ) -> User:
    
    user.set_password(password)

    user.full_clean()
    user.save()

    return user


def generate_verification_token(user: User) -> uuid.UUID:

    if user.is_verified:
        raise UserAlreadyVerified()

    user.verification_token = uuid.uuid4()
    user.verification_sent_at = timezone.now()

    user.full_clean()
    user.save(update_fields=['verification_token', 'verification_sent_at'])
    
    return user.verification_token


def verify_email_token(token: uuid.UUID) -> None:

    try:
        user = User.objects.get(verification_token=token)
    except User.DoesNotExist:
        raise VerificationTokenInvalid()

    is_expired = (
        user.verification_sent_at is None
        or timezone.now() > user.verification_sent_at + timezone.timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRATION_HOURS)
    )

    if is_expired:
        raise VerificationTokenExpired()

    user.is_verified = True
    user.verification_token = None

    user.full_clean()
    user.save(update_fields=['is_verified', 'verification_token'])


def delete_expired_unverified_users():
    settings_obj = SiteConfig.load()

    deadline = timezone.now() - timedelta(
        days=settings_obj.unverified_user_ttl_days
    )

    deleted_count, _ = User.objects.filter(
        is_verified=False,
        created_at__lt=deadline,
    ).delete()

    return {
        'deleted_users_count': deleted_count,
    }