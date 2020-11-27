from marshmallow import Schema, fields


class AuthenticationInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CustomerInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CustomerUpdateInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)


class ChangePasswordUpdateInputSchema(Schema):
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)
