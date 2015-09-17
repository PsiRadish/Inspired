import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    TUMBLR_CLIENT = os.environ['TUMBLR_CLIENT']
    TUMBLR_SECRET = os.environ['TUMBLR_SECRET']
    TUMBLR_REQUEST_URL      = 'http://www.tumblr.com/oauth/request_token'
    TUMBLR_AUTH_BASE_URL    = 'http://www.tumblr.com/oauth/authorize'
    TUMBLR_ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'
    TUMBLR_CALLBACK_URL = None
    SQLALCHEMY_DATABASE_URI = None
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/Inspired"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TUMBLR_CALLBACK_URL = "http://localhost:5000/user/dash/tumblr"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/Inspired"
    

class ProductionConfig(Config):
    DEBUG = False
    TUMBLR_CALLBACK_URL = "https://infinspired.herokuapp.com//user/dash/tumblr"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    