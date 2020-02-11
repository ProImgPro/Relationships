import os
os_env =os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration"""
    # app config
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLE = False
    TEMPLATE_AUTO_RELOAD =False
    # Celery background task config
    CELERY_BROKEN_URL = 'redis://hostlocal:27017'
    CELERY_BACKEND_URL = 'redis://hostlocal:27017'
    #JWT config
    JWT_SECRET_KEY = 'JONE'
    JWT_BLACKLIST_ENABLE = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # Mongo config
    MONGO_DBNAME = 'Relationship'
    MONGO_HOST = 'hostlocal'
    MONGO_CONNECT = False

