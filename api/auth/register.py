
from flask.helpers import url_for
from api.auth.utils import create_token
from api.utils.response import restify
from api.auth.errors import DuplicateUserError, SchemaValidationError
from .auth import api, crypt
from uuid import uuid4
import validators

from db import create_user, get_user
from utils import validator
from api.user.models import User, user_from_dict

from flask_restful import Resource, reqparse


@api.resource('/register')
class UserRegisterResource(Resource):
    """Registers a new user on the site"""

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True)
        self.parser.add_argument('password', required=True)
        self.parser.add_argument('first_name', required=True)
        self.parser.add_argument('last_name', default='')

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']
        first_name = args['first_name']
        last_name = args['last_name']

        # Validate fields
        errors = dict()
        if not validators.email(email):
            errors['email'] = "Provide a valid email"
        if not validators.length(first_name, min=3):
            errors['first_name'] = "'first_name' should be a minimum of 3 characters"

        pr = validator.password(password)
        if not pr:
            errors['password'] = pr.message

        # TODO: Add extra validation
        if errors:
            return SchemaValidationError(errors)

        # Attempt to fetch user with that email
        if get_user(email=email) != None:
            return DuplicateUserError

        user = User(email=email, password=crypt.generate_password_hash(password).decode(),
                    first_name=first_name, last_name=last_name)

        user = create_user(user.to_dict())
        if 'error' in user:
            return (restify(False, "An error occurred"), 500)
        
        # Since no errors, send verification email to user

        return (restify(True, "user registered successfully"), 201)
