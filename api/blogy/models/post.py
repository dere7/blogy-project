#!/usr/bin/env python3
"""Post model"""
from datetime import datetime
from mongoengine import *
from .. import db
from .user import User


class Comment(EmbeddedDocument):
    """Comment embedded model"""
    user = ReferenceField(User, required=True)
    content = StringField(max_length=130, required=True)
    created_at = DateTimeField(default=datetime.now())


class Post(db.Document):
    """Post model"""
    title = StringField(max_length=255, required=True)
    body = StringField(max_length=255, required=True)
    author = ReferenceField(User, required=True)
    published_at = DateTimeField(required=True)
    tags = ListField(StringField(50), max_length=10, default=list)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)
    likes = IntField(default=0, min_value=0)
    cover_pic = URLField()
    is_published = BooleanField(default=True)
