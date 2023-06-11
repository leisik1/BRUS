from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(format="%Y-%m-%d")

class PlainGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    group_id = fields.Int(required=True, load_only=True)
    group = fields.Nested(PlainGroupSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    date = fields.Date(format="%Y-%m-%d")
    group_id = fields.Int()

class GroupSchema(PlainGroupSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    group_id = fields.Int(load_only=True)
    group = fields.Nested(PlainGroupSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
