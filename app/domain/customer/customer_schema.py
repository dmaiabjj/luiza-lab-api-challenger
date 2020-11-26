from marshmallow import Schema, fields


class CustomerInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
