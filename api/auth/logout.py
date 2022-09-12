from api.utils.response import restify
from db import revoke_jwt
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt
from flask_restful import Resource

from .auth import api


@api.resource('/logout')
class UserLogoutResource(Resource):
    """Logs the user out and revokes the tokens associated with this session"""


    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        acc = get_raw_jwt()['jti']
        ref = None
        if 'refresh_token' in claims:
            ref = claims['refresh_token']
            revoke_jwt(ref)
        revoke_jwt(acc)
        return (restify(True, "Signed out successfully"), 200)
