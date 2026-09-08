from drf_spectacular.utils import inline_serializer

from rest_framework import serializers


def success_schema(serializer_class, many=False):
    return inline_serializer(
        name=f"Success{serializer_class.__name__}",
        fields={
            "success": serializers.BooleanField(),
            "data": serializer_class(many=many),
            "errors": serializers.JSONField(
                allow_null=True,
                required=False,
            ),
        },
    )