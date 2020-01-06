from marshmallow import Schema, fields, pre_load, post_load
from marshmallow import EXCLUDE
from marshmallow import ValidationError


class BaseSchema(Schema):
    @post_load
    def remove_none_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value and value != 'None'
        }

    class Meta:
        # ignore unknown params
        unknown = EXCLUDE


class User(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    screen_name = fields.String()
    location = fields.String(allow_none=True)
    url = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    protected = fields.Boolean()
    verified = fields.Boolean()
    followers_count = fields.Integer()
    friends_count = fields.Integer()
    listed_count = fields.Integer()
    favourites_count = fields.Integer()
    statuses_count = fields.Integer()
    created_at = fields.DateTime(format='%a %b %d %H:%M:%S %z %Y')
    default_profile = fields.Boolean()
    default_profile_image = fields.Boolean()


class Tweet(BaseSchema):
    id = fields.Int()
    created_at = fields.DateTime(format='%a %b %d %H:%M:%S %z %Y')
    text = fields.String()
    source = fields.String()
    truncated = fields.Boolean()
    in_reply_to_status_id = fields.Integer(allow_none=True)
    in_reply_to_user_id = fields.Integer(allow_none=True)
    in_reply_to_screen_name = fields.String(allow_none=True)
    coordinates = fields.String(allow_none=True)
    place = fields.String(allow_none=True)
    is_quote_status = fields.Boolean()
    quoted_status_id = fields.Integer()
    is_retweet_status = fields.Boolean()
    retweeted_status_id = fields.Integer()
    quote_count = fields.Integer()
    reply_count = fields.Integer()
    retweet_count = fields.Integer()
    favorite_count = fields.Integer()
    entities = fields.String()
    extended_entities = fields.String()
    possibly_sensitive = fields.Boolean()
    filter_level = fields.String()
    lang = fields.String()
    source_type = fields.String()
    source_id = fields.Int()
    user_id = fields.Integer()

    @pre_load
    def preporcess_dicts(self, in_data, **kwargs):
        in_data['extended_entities'] = str(in_data.get('extended_entities'))
        in_data['entities'] = str(in_data.get('entities'))
        in_data['coordinates'] = str(in_data.get('coordinates'))
        in_data['place'] = str(in_data.get('place'))
        return in_data
