import os 

from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path

from django_scalar.views import scalar_viewer
from drf_spectacular.views import SpectacularAPIView

from apps.posts.views import PostFeedApi


urlpatterns = [
    path('api/v1/auth/', include('apps.auth.urls')),
    path('api/v1/posts/', include('apps.posts.urls')),
    path('api/v1/settings/', include('apps.core.urls')),
    path('api/v1/feed', PostFeedApi.as_view(), name='post-feed'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', scalar_viewer, name='scalar-viewer')
]


if os.environ.get('DJANGO_ENV', 'local').lower() == 'local':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
