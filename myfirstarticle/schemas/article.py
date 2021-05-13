from marshmallow import Schema, fields
from .base import PaginationSchema


class ArticleSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    short_description = fields.String(required=True)
    long_description = fields.String(required=True)
    published = fields.Boolean(default=False)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)


class ArticlePaginationSchema(PaginationSchema):
    results = fields.Nested(ArticleSchema, many=True)
