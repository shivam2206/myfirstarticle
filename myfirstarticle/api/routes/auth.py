import json

from flask import request
from flask_apispec import marshal_with
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from ...model import Author
from ...schemas.auth import *
from ...schemas.base import SuccessSchema, BaseRemoveSchema
from ...utils.decorators import add_pagination
from ...utils.helper import encode_auth_token, decode_auth_token
from ...database import db


@doc(tags=['Auth'])
class AuthLoginAPI(MethodResource, Resource):

    @use_kwargs(AuthSchema, location="json")
    @marshal_with(TokenSchema)
    def post(self, **kwargs):
        author = Author.query.filter_by(email=kwargs['email']).first()
        if author is not None and author.verify_password(kwargs['password']):
            token = encode_auth_token(author.id)
            return {"status": "success", "token": token}
        else:
            return {"status": "failed", "message": "Invalid credentials"}, 401
