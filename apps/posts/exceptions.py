from apps.core.exceptions import NotFoundException, ValidationException


class PostNotFound(NotFoundException):
    default_message = 'Пост не найден.'


class CommentNotFound(NotFoundException):
    default_message = 'Комментарий не найден.'


class PostAlreadyLiked(ValidationException):
    default_message = 'Пост уже лайкнут.'


class PostCannotBeLiked(ValidationException):
    default_message = 'Нелья лайкать/дизлайкать свой собственный пост.'