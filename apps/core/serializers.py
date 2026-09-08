from rest_framework import serializers

from .models import SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteConfig
        fields = ['unverified_user_ttl_days', 'post_ttl_days']