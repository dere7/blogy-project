#!/usr/bin/env python3
"""Post model"""
from datetime import datetime
from mongoengine import *
from . import db
from .user import User


class Comment(db.EmbeddedDocument):
    """Comment embedded model"""
    user = db.ReferenceField(User, required=True)
    content = db.StringField(max_length=130, required=True)
    created_at = db.DateTimeField(default=datetime.now())


class Post(db.Document):
    """Post model"""
    title = db.StringField(max_length=255, required=True)
    body = db.StringField(max_length=255, required=True)
    author = db.ReferenceField(User, required=True)
    published_at = db.DateTimeField(required=True)
    tags = db.ListField(StringField(max_length=50),
                        max_length=10, default=list)
    comments = db.ListField(EmbeddedDocumentField(Comment), default=list)
    likes = db.IntField(default=0, min_value=0)
    cover_pic = db.URLField()
    is_published = db.BooleanField(default=True)
