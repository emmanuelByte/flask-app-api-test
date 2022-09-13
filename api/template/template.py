from math import ceil
from re import template
from api.auth.errors import SchemaValidationError, TemplateDoesNotExistError
from api.template.models import Template, template_from_dict
from flask import Blueprint,request
from flask.globals import current_app, g
from api.utils.misc import PaginationMeta,max_per_page
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.local import LocalProxy
from db import create_template, create_user, delete_template, get_template, get_templates, get_user, update_template
from api.utils.response import restify


template = Blueprint('template', __name__, url_prefix='/api/v1/template')
api = Api(template)


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


@api.resource('', '/<string:template_id>')  # /api/v1/template
class TemplateResource(Resource):
    """Update or retrieve template's details"""

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'body', required=True, help="Body cannot be blank!", location='json', type=str)
        self.parser.add_argument('template_name', required=True,
                                 help="Template name cannot be blank!", location='json', type=str)
        self.parser.add_argument(
            'subject', required=True, help="Subject cannot be blank!", location='json', type=str)

    @jwt_required
    def get(self, template_id=None):
        uid = get_jwt_identity()
        if template_id is not None:

            template = get_template(template_id)
            if template == None:
                return TemplateDoesNotExistError

            # Convert to app usable model
            template = Template.from_dict(template)
            # print(template.author!=uid)
            if template.author != uid:
                return TemplateDoesNotExistError

            return restify(True, "Template retrieved successfully", dict(template=template.to_dict()))
        else:

            limit = int(max_per_page)

            page = request.args.get('page', 1)

            try:

                page = int(page)

            except:

                page = 1

            if page < 1:

                page = 1

            # Build filters to use

            filters = dict()

            res_templates, total = get_templates(

                uid, page=page, limit=limit, filters=filters)

            meta = PaginationMeta(current_page=page, first_page=1,

                                  last_page=max(1, ceil(total / limit)),

                                  amount_per_page=limit, total_amount=total)

            for template in res_templates:

                template['_id'] = str(template['_id'])

            return restify(True, "Templates retrieved successfully",

                           data=dict(templates=res_templates, meta=meta.to_dict()))

    @jwt_required
    def post(self, template_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'body', required=True, help="Body cannot be blank!", location='json', type=str)
        parser.add_argument('template_name', required=True,
                            help="Template name cannot be blank!", location='json', type=str)
        parser.add_argument('subject', required=True,
                            help="Subject cannot be blank!", location='json', type=str)
        args = parser.parse_args()
        subject = args['subject']
        template_name = args['template_name']
        body = args['body']

        # Validate fields
        errors = dict()

        uid = get_jwt_identity()

        # TODO: Add extra validation
        if errors:
            return SchemaValidationError(errors)

        template = Template(
            subject=subject, template_name=template_name, body=body, author=uid)
        template = create_template(template.to_dict())
        if 'error' in template:
            return (restify(False, "An error occurred"), 500)

        return restify(True, "Template created successfully", dict(template=template))

    @jwt_required
    def put(self, template_id):

        parser = reqparse.RequestParser()
        parser.add_argument('body',  location='json', type=str)
        parser.add_argument('template_name',   location='json', type=str)
        parser.add_argument('subject',  location='json', type=str)
        args = parser.parse_args()
        subject = args['subject']
        template_name = args['template_name']
        body = args['body']

        # Validate fields
        errors = dict()

        update_obj = dict()
        if subject:
            update_obj['subject'] = subject

        if template_name:
            update_obj['template_name'] = template_name

        if body:
            update_obj['body'] = body


        uid = get_jwt_identity()

        # TODO: Add extra validation
        if errors:
            return SchemaValidationError(errors)

        template = get_template(template_id)
        template = template_from_dict(template)
        if template.author != uid:
            return TemplateDoesNotExistError

        template = update_template(template_id, update_obj)
        if 'error' in template:
            return (restify(False, "An error occurred"), 500)

        return restify(True, "Template created successfully", dict(template=template))
    @jwt_required
    def delete(self, template_id):
        uid = get_jwt_identity()

        template = get_template(template_id)
        if template == None:
                return TemplateDoesNotExistError

        # Convert to app usable model
        template = Template.from_dict(template)
        # print(template.author!=uid)
        if template.author != uid:
            return TemplateDoesNotExistError
        t=delete_template(template_id)    
        return restify(True, "Template deleted successfully", dict(template=template.to_dict()))

        