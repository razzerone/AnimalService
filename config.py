from os import environ

DEBUG: bool = bool(environ.get('DEBUG'))

KEY_SERVICE_URL: str = environ.get('KEY_SERVICE_URL')

MYSQL_URL: str = environ.get('MYSQL_URL')
MYSQL_USER: str = environ.get('MYSQL_USER')
MYSQL_PASSWORD: str = environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE: str = environ.get('MYSQL_DATABASE')


