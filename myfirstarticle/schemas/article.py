from marshmallow import Schema, fields

from .author import AuthorSchema
from .base import PaginationSchema, BaseUpdateSchema
from marshmallow.validate import Length


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(min=5, max=100), description="The title of the Article")
    short_description = fields.String(required=True, validate=Length(max=300),
                                      description="Short description for preview")
    long_description = fields.String(required=True, description="Full content of the Article")
    created_on = fields.DateTime(dump_only=True, description="Article creation date time")
    modified_on = fields.DateTime(dump_only=True, description="Recent Article modification date time")
    author = fields.Nested(AuthorSchema)


class ArticlePaginationSchema(PaginationSchema):
    results = fields.Nested(ArticleSchema, many=True)


class ArticleUpdateSchema(Schema):
    id = fields.Integer(required=True, description="Id of the Article")
    title = fields.String(validate=Length(min=5, max=100), description="Article title")
    short_description = fields.String(required=True, validate=Length(max=300),
                                      description="Short description for preview")
    long_description = fields.String(required=True, description="Full content of the Article")
