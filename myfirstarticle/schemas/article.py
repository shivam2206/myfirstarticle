from marshmallow import Schema, fields
from .base import PaginationSchema
from marshmallow.validate import Length


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(max=100), description="The title of the Article")
    short_description = fields.String(required=True, validate=Length(max=300),
                                      description="Short description for preview")
    long_description = fields.String(required=True, description="Full content of the Article")
    published = fields.Boolean(default=False, description="Indicates if the Article is live")
    created_on = fields.DateTime(dump_only=True, description="Article creation date time")
    modified_on = fields.DateTime(dump_only=True, description="Recent Article modification date time")


class ArticlePaginationSchema(PaginationSchema):
    results = fields.Nested(ArticleSchema, many=True)
