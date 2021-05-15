from marshmallow import Schema, fields

__all__ = ['AuthSchema', 'TokenSchema']


class AuthSchema(Schema):
    email = fields.String(required=True, load_only=True, description="Author Email")
    password = fields.String(required=True, load_only=True, description="Account password")


class TokenSchema(Schema):
    token = fields.String(dump_only=True, description="JWT Auth token")
    status = fields.String(dump_only=True, description="Request status")
