from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField

"""

Define you MongoEngine Models here

"""
class User(Document):
    name = StringField()
    email = StringField()

    meta = {'collection' : 'User', 'allow_inheritance' : False}

