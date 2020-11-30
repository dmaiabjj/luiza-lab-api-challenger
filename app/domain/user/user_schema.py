from marshmallow import Schema, fields, validate

from app.domain.user.user import RoleCategory


class UserAuthenticationInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    roles = fields.List(fields.String(
        validate=validate.OneOf(choices=[r.name for r in RoleCategory]), required=True), required=False)


class UserUpdateInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    roles = fields.List(fields.String(
        validate=validate.OneOf(choices=[r.name for r in RoleCategory]), required=True), required=False)


class UserChangePasswordUpdateInputSchema(Schema):
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)
