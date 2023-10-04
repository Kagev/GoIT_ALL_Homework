from mongoengine import Document, StringField, ReferenceField, ListField, BooleanField, DateField
import random


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(required=True)
    author = ReferenceField(Author)
    quote = StringField()


class Contact(Document):
    fullname = StringField(required=True)
    born_date = DateField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    prefer_sms = BooleanField(default=False)

    meta = {
        'collection': 'contacts'
    }
