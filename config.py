import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId, json_util
from flask.json import JSONEncoder
from datetime import timedelta
load_dotenv()


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


class Config(object):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
    CSRF_ENABLED = True
    MONGODB_DATABASE_URI = os.environ.get("DATABASE_URL")
    MONGODB_DATABASE_NAME = os.environ.get("DATABASE_NAME")
    
   
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_USER_CLAIMS = 'user_claims'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ('access', 'refresh')
    RESTFUL_JSON = dict(ensure_ascii=False, indent=4, separators=(',', ': '), cls=MongoJsonEncoder)


class ProductionConfig(Config):
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.gmail.com'
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(Config):
   
    ENV = "development"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "secret_for_test_environment"

