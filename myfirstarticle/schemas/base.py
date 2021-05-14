from marshmallow import Schema, fields
from marshmallow.validate import Range

from myfirstarticle.settings import MAX_PAGE_ITEMS


class PaginationSchema(Schema):
    count = fields.Integer(dump_only=True, description="Total number of records")
    limit = fields.Integer(default=MAX_PAGE_ITEMS, description="Maximum records per page")
    has_next = fields.Boolean(default=False, description="Next page is available")
    has_previous = fields.Boolean(default=False, description="Previous page is available")


class BaseUpdateSchema(Schema):
    id = fields.Integer()

    def __init__(self, *args, **kwargs):
        super(BaseUpdateSchema, self).__init__(*args, **kwargs)
        _declared_fields = self._declared_fields
        for field in _declared_fields:
            if field == "id":
                _declared_fields[field].required = True
                _declared_fields[field].dump_only = False
            else:
                _declared_fields[field].required = False


class BaseRemoveSchema(Schema):
    id = fields.Integer(required=True, validate=Range(min=1), description="Unique id of the record")


class SuccessSchema(Schema):
    message = fields.String(dump_only=True)
    status = fields.String(dump_only=True, default="success")
