from apps.core.exceptions import ValidationException 


class VerificationTokenExpired(ValidationException):
    default_message = 'Срок действия токена истек.'


class UserAlreadyVerified(ValidationException):
    default_message = 'Пользователь уже подтвержден.'


class VerificationTokenInvalid(ValidationException):
    default_message = 'Неверный токен подтверждения.'