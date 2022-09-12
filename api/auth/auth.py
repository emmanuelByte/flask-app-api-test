from flask import Blueprint
from flask.globals import current_app, g
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from werkzeug.local import LocalProxy


auth = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')
api = Api(auth)


def get_bcrypt():
    bcrypt = getattr(g, '_bcrypt', None)
    if bcrypt is None:
        bcrypt = g._bcrypt = current_app.config['BCRYPT']
    return bcrypt


def get_jwt():
    jwt = getattr(g, '_jwt', None)
    if jwt is None:
        jwt = g._jwt = current_app.config['JWT']

    return jwt


jwt: JWTManager = LocalProxy(get_jwt)
crypt: Bcrypt = LocalProxy(get_bcrypt)

from . import register
from . import login
from . import logout
