from marshmallow import Schema, fields
from marshmallow.validate import Length

from .author import AuthorSchema
from .base import PaginationSchema

__all__ = ['ArticleSchema', 'ArticlePaginationSchema', 'ArticleUpdateSchema', 'ArticleGetSchema']


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(min=5, max=100), description="The title of the Article")
    short_description = fields.String(required=True, validate=Length(max=300),
                                      description="Short description for preview")
    long_description = fields.String(required=True, description="Full content of the Article")
    created_on = fields.DateTime(dump_only=True, description="Article creation date time")
    modified_on = fields.DateTime(dump_only=True, description="Recent Article modification date time")
    author = fields.Nested(AuthorSchema, dump_only=True)


class ArticlePaginationSchema(PaginationSchema):
    results = fields.Nested(ArticleSchema, many=True)


class ArticleUpdateSchema(Schema):
    id = fields.Integer(required=True, description="Id of the Article")
    title = fields.String(validate=Length(min=5, max=100), description="Article title")
    short_description = fields.String(validate=Length(min=1, max=300),
                                      description="Short description for preview")
    long_description = fields.String(description="Full content of the Article")


class ArticleGetSchema(Schema):
    id = fields.Integer(load_only=True, description="Search a Article by its id")
    author_id = fields.Integer(load_only=True, description="Search Articles published by the specific author")
