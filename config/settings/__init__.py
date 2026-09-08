import os 


DJANGO_ENV = os.environ.get('DJANGO_ENV', 'local').lower()


if DJANGO_ENV == 'prod':
    from .prod import *
else:
    from .local import *