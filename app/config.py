import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_can_never_guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'SECRET_KEY'


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/unusual_spending'

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    SQLALCHEMY_ECHO = False
Config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
}
