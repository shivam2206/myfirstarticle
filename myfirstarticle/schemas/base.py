from marshmallow import Schema, fields

from myfirstarticle.settings import MAX_PAGE_ITEMS


class PaginationSchema(Schema):
    count = fields.Integer(dump_only=True, description="Total number of records")
    limit = fields.Integer(default=MAX_PAGE_ITEMS, description="Maximum records per page")
    has_next = fields.Boolean(default=False, description="Next page is available")
    has_previous = fields.Boolean(default=False, description="Previous page is available")
