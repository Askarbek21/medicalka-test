from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response

from apps.core.exceptions import DomainException


# Hacksoft inspired custom exception handler
def custom_exception_handler(exc, context):

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, context)

    if isinstance(exc, DomainException):
        return Response(
            {
                'success': False,
                'data': None,
                'errors': [
                    {
                        'message': exc.message,
                    }
                ],
            },
            status=exc.status_code,
        )

    if response is None:
        return response

    if isinstance(exc, exceptions.ValidationError):
        errors = []

        for field, messages in response.data.items():
            for message in messages:
                errors.append(
                    {
                        'field': field,
                        'message': str(message),
                    }
                )

        response.data = {
            'success': False,
            'data': None,
            'errors': errors,
        }

        return response

    detail = response.data.get('detail', 'Unknown error')

    response.data = {
        'success': False,
        'data': None,
        'errors': [
            {
                'message': str(detail),
            }
        ],
    }

    return response