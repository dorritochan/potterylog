from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()

class PotSchema(Schema):
    id = fields.Integer()
    vessel_type = fields.String()