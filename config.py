from os import environ

DEBUG: bool = bool(environ.get('DEBUG'))

KEY_SERVICE_URL: str = environ.get('KEY_SERVICE_URL')

DB_HOST: str = environ.get('DB_HOST')
DB_PORT: str = environ.get('DB_PORT')
DB_USER: str = environ.get('DB_USER')
DB_PASSWORD: str = environ.get('DB_PASSWORD')
DB_NAME: str = environ.get('DB_NAME')


