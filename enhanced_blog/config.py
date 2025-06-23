import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
