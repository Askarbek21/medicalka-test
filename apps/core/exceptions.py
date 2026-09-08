class DomainException(Exception):
    status_code = 400
    default_message = 'Ошибка доменной логики.'

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundException(DomainException):
    status_code = 404
    default_message = 'Не найдено.'


class ValidationException(DomainException):
    status_code = 400
    default_message = 'Ошибка валидации.'


class PermissionDeniedException(DomainException):
    status_code = 403
    default_message = 'Доступ запрещен.'


class AuthenticationFailedException(DomainException):
    status_code = 401
    default_message = 'Ошибка аутентификации.'