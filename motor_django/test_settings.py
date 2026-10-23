from .settings import *


# Esta base en memoria solo se usa al ejecutar las pruebas automatizadas.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
