from api.utils.response import restify
from api.auth.errors import InvalidCredentialsError, SchemaValidationError
import validators
from api.user.models import User
from db import get_user
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from flask_restful import Resource, reqparse
from utils import validator

from .auth import api, crypt


@api.resource('/login')
class UserLoginResource(Resource):
    """Generates an authentication token to make authenticated requests for the user"""

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True)
        self.parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        # Validate fields
        errors = dict()
        if not validators.email(email):
            errors['email'] = "Provide a valid email"

        pr = validator.password(password, min_length=3)
        if not pr:
            errors['password'] = pr.message

        # TODO: Add extra validation
        if errors:
            return SchemaValidationError(errors=errors)

        # Attempt to fetch user with that email
        user = get_user(email=email)
        if user == None:
            return InvalidCredentialsError
        user = User.from_dict(user)

        if not crypt.check_password_hash(user.password, password):
            return InvalidCredentialsError

        access_token = create_access_token(
            user.id )

        duser = user.to_dict()
        if 'password' in duser:
            del duser['password']
        return (restify(True, "User signed in successfully",
                        data={
                            'user': duser,
                            'access_token': access_token,
                        }), 200)
