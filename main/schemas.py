from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    contactName = fields.Str(required=True)
    email = fields.Str(required=True)
    imageFile = fields.Str()
    password = fields.Str(load_only=True)
    phoneNumber = fields.Str(required=True)
    ads = fields.Nested('AdSchema', many=True, exclude=('userId', ))


class PayingTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)


class AdSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    datePosted = fields.DateTime(dump_only=True)
    userId = fields.Int()
    images = fields.Nested('ImageSchema', many=True)
    payingTypes = fields.Nested(PayingTypeSchema, many=True)
    books = fields.Nested('BookSchema', many=True)


class ImageSchema(Schema):
    id = fields.Int(dump_only=True)
    imageFile = fields.Str(required=True)
    adId = fields.Int()


class LikesSchema(Schema):
    id = fields.Int(dump_only=True)
    userId = fields.Nested(UserSchema, only=['id'])
    adId = fields.Nested(AdSchema, only=['id'])


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    price = fields.Int()
    adId = fields.Int()




