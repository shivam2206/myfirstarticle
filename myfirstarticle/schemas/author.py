from marshmallow import Schema, fields
from .base import PaginationSchema, BaseUpdateSchema
from marshmallow.validate import Length

__all__ = ['AuthorSchema', 'AuthorPaginationSchema', 'AuthorUpdateSchema']


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Length(min=1, max=100), description="Author name")
    email = fields.String(required=True, validate=Length(min=2, max=100),
                          description="Author Email, Cannot be changed later")
    password = fields.String(required=True, load_only=True, validate=Length(min=4, max=16),
                             description="Account password")


class AuthorPaginationSchema(PaginationSchema):
    results = fields.Nested(AuthorSchema, many=True)


class AuthorUpdateSchema(BaseUpdateSchema, AuthorSchema):
    pass
