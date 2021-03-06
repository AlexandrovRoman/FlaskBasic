from os import environ, path

here = path.abspath(path.dirname(__file__))
template_folder = path.join(path.split(here)[0], "templates")
static_folder = path.join(path.split(here)[0], "static")

HOST = environ.get('HOST', '127.0.0.1')
PORT = int(environ.get('PORT', 5000))
user = environ.get('DB_USERNAME', 'postgres')
url = environ.get('DB_URL', 'localhost:5432')
db = environ.get('DB_NAME', 'PFRProject')
password = environ.get('DB_PASSWORD', '')


class BaseConfig:
    WTF_CSRF_SECRET_KEY = environ.get('WTF_CSRF_SECRET_KEY', 'dsofpkoasodksap')
    SECRET_KEY = environ.get('SECRET_KEY', 'zxczxasdsad')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{url}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT', 'iufsdivdjkvcbadb')
    EMAIL_SENDER_LOGIN = 'pfrproject2020@gmail.com'
    EMAIL_SENDER_PASSWORD = environ.get('EMAIL_SENDER_PASSWORD', '')
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "cdrrftpocfpreio")
    JSON_AS_ASCII = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = True


class DevelopConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True


Config = ProductionConfig
