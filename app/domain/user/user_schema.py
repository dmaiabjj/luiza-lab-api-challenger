from marshmallow import Schema, fields


class UserAuthenticationInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserUpdateInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)


class UserPasswordUpdateInputSchema(Schema):
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)
