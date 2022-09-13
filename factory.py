import os

from flask import Flask
from flask import jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import config
from api.auth.auth import auth as auth_blueprint
from api.user.user import user as user_blueprint
from api.template.template import template as template_blueprint
from db import is_token_revoked


CONFIGURATIONS = {
    'production': config.ProductionConfig,
    'development': config.DevelopmentConfig,
}


def create_app():
    # APP_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    
    app.config.from_object(CONFIGURATIONS.get(os.getenv('APP_ENV', 'development')))
    app.json_encoder = config.MongoJsonEncoder
    CORS(app)

    # register blue prints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(template_blueprint)


    jwt = JWTManager(app)

    app.config['JWT'] = jwt
    app.config['BCRYPT'] = Bcrypt(app)

    @app.context_processor
    def inject_globals():
        return dict(SITE_DOMAIN=app.config.get('SITE_DOMAIN', 'test.com'))

    @jwt.token_in_blacklist_loader
    def check_token_blacklisted(jwt) -> bool:
        return is_token_revoked(jwt['jti'])

    @jwt.expired_token_loader
    def expired_token(_):
        return make_response(jsonify({'success': False, 'message': 'Expired authorization token.', 'error_code': 'expired_token'}), 401)
    
    @jwt.invalid_token_loader
    def invalid_token(reason):
        return make_response(jsonify({'success': False, 'message': "Invalid authorization token: {}".format(reason), 'error_code': 'bad_token'}), 422)

    @jwt.revoked_token_loader
    @jwt.needs_fresh_token_loader
    def fresh_token():
        return make_response(jsonify({'success': False, 'message': 'Invalid authorization token.', 'error_code': 'bad_token'}), 401)

    @jwt.unauthorized_loader
    def unauthorized(_):
        return make_response(jsonify({'success': False, 'message': 'Authorization is required.', 'error_code': 'bad_token'}), 401)


    return app
