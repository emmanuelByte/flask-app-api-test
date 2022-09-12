from api.auth.errors import UserDoesNotExistError
from api.user.models import User
from flask import Blueprint
from flask.globals import current_app, g
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.local import LocalProxy
from db import get_user, update_user
from api.utils.response import restify


user = Blueprint('user', __name__, url_prefix='/api/v1/user')
api = Api(user)


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

@api.resource('')
class UserResource(Resource):
    """Update or retrieve user's details"""

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name')
        self.parser.add_argument('last_name')

    @jwt_required
    def get(self):
        uid = get_jwt_identity()

        user = get_user(uid)
        if user == None:
            return UserDoesNotExistError
        
        # Convert to app usable model
        user = User.from_dict(user).to_dict()

        if 'password' in user:
            del user['password']

        return restify(True, "User retrieved successfully", dict(user=user))

