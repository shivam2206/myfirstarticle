from marshmallow import Schema, fields

from myfirstarticle.settings import MAX_PAGE_ITEMS


class PaginationSchema(Schema):
    count = fields.Integer(dump_only=True)
    limit = fields.Integer(default=MAX_PAGE_ITEMS)
    has_next = fields.Boolean(default=False)
    has_previous = fields.Boolean(default=False)
