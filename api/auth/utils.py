from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_jwt_extended.config import config
from flask_jwt_extended.utils import decode_token, verify_token_not_blacklisted
from jwt import InvalidTokenError


def create_token(identity, expires_delta=None, token_type=None):
    token = create_access_token(identity, expires_delta=expires_delta or timedelta(days=1), user_claims={'__token_type__': token_type})
    return token



def verify_token(token, token_type):
    decoded_token = decode_token(token)
    verify_token_not_blacklisted(decoded_token, 'access')
    if decoded_token.get(config.user_claims_key, {}).get('__token_type__') != token_type:
        raise InvalidTokenError
    return decoded_token


