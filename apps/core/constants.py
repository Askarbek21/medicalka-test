class Tags:
    AUTH = 'Авторизация'
    POSTS = 'Посты'
    COMMENTS = 'Комментарии'
    SETTINGS = 'Настройки'


SPECTACULAR_TAGS = [
    {'name': Tags.AUTH, 'description': 'Вход, выход, обновление токена, текущий пользователь и т.п.'},
    {'name': Tags.POSTS, 'description': 'Операции с постами.'},
    {'name': Tags.SETTINGS, 'description': 'Операции с настройками сайта (нужны админ права)'},
    {'name': Tags.COMMENTS, 'description': 'Операции с комментариями.'},
]