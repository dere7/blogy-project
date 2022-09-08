'''post model'''
from datetime import datetime as dt
from slugify import slugify
from mongoengine import (
    EmbeddedDocument,
    ReferenceField,
    StringField,
    DateTimeField,
    URLField,
    BooleanField,
    ListField,
    EmbeddedDocumentListField,
    CASCADE
)
from blogy import db
from .user import User


class Comment(EmbeddedDocument):
    '''comment model'''
    user = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=dt.utcnow)

    def to_dict(self):
        '''dict repr of obj'''
        return {
            'user': self.user.to_dict(),
            'content': self.content,
            'created_at': self.created_at
        }


class Post(db.Document):
    '''post model'''
    slug = StringField(min_length=5, max_length=255)
    title = StringField(max_length=255, min_length=5, required=True)
    body = StringField(required=True)
    author = ReferenceField(
        User, required=True, reverse_delete_rule=CASCADE)
    cover_pic = URLField()
    is_published = BooleanField(default=False)
    tags = ListField(StringField(max_length=70))
    created_at = DateTimeField(default=dt.utcnow)
    updated_at = DateTimeField(default=dt.utcnow)
    published_at = DateTimeField()
    comments = EmbeddedDocumentListField(Comment)

    meta = {'indexes': ['slug']}

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        if 'slug' not in kwargs:
            self.slug = slugify(self.title)
        if kwargs['is_published']:
            self.published_at = dt.utcnow()

    def to_dict(self):
        '''get dict of the obj'''
        return {
            'slug': self.slug,
            'title': self.title,
            'body': self.body,
            'author': self.author.to_dict(),
            'cover_pic': self.cover_pic,
            'published_at': self.published_at,
            'is_published': self.is_published,
            'comments': [comment.to_dict() for comment in self.comments],
            'tags': self.tags
        }
