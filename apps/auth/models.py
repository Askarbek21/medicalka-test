from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models

from apps.core.models import BaseModel

from .managers import UserManager


class User(AbstractBaseUser, BaseModel):
    full_name = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(3)]
    )
    username = models.CharField(
        max_length=32, 
        validators=[MinLengthValidator(3)], 
        unique=True
    )
    verification_token = models.UUIDField(
        null=True, 
        blank=True,
        editable=False
    )
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    email = models.EmailField(unique=True)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['full_name', 'email']

    objects = UserManager()


    def __str__(self):
        return self.username



