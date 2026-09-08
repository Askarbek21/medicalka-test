from django.urls import path 

from .views import *


urlpatterns = [
    path('', SiteConfigApi.as_view(), name='site-config'),
    path('delete-expired-posts/', DeleteExpiredPostsApi.as_view(), name='delete-expired-posts'),
    path('delete-expired-unverified-users/', DeleteExpiredUnverifiedUsersApi.as_view(), name='delete-expired-unverified-users'),
]