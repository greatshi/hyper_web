import time
import datetime

from django_mongoengine import fields
from django_mongoengine import Document, EmbeddedDocument


# Create your models here.
class User(Document):
    created_time = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    user_name = fields.StringField(max_length=250)
    phone_num = fields.StringField(default='', max_length=250)
    phone_zone_code = fields.StringField(default='', max_length=250)
    password = fields.StringField(default='', max_length=250)

    address = fields.StringField(default='', max_length=250)
    access_token = fields.StringField(default='', max_length=250)
    password_site = fields.StringField(default='', max_length=250)
    client_id = fields.StringField(default='', max_length=250)
    client_secret = fields.StringField(default='', max_length=250)
    expires_in = fields.IntField(default=7200)

    def __unicode__(self):
        return self.user_name


class WebTxLocal(Document):
    sender = fields.StringField(max_length=250)
    page_hash = fields.StringField(max_length=250)
    page_name = fields.StringField(max_length=250)
    last_page_hash = fields.StringField(max_length=250)
    timestamp = fields.IntField(default=0)
    page_content = fields.StringField(default='', max_length=2000000)

    def __unicode__(self):
        return self.page_hash
