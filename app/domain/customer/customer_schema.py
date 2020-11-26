from marshmallow import Schema, fields


class CustomerInputSchema(Schema):
    title = fields.Str(required=True)
    note = fields.Str(required=True)
    user_id = fields.Int(required=True)
    time_created = fields.DateTime(required=True)
