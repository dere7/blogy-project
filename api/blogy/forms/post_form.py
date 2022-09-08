'''post forms'''
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, BooleanField, FieldList
from wtforms.validators import Length, URL, Optional, DataRequired
from blogy.models.post import Post


CreatePostForm = model_form(
    Post, only=['title', 'body', 'cover_pic', 'is_published', 'tags'])


class CommentForm(FlaskForm):
    '''comment form'''
    content = StringField(validators=[Length(min=3), DataRequired()])


class UpdatePostForm(FlaskForm):
    '''update post form'''
    title = StringField(validators=[Length(min=5, max=255), Optional()])
    body = StringField()
    cover_pic = URLField(validators=[URL(), Optional()])
    is_published = BooleanField()
    tags = FieldList(StringField(Length(max=70)))
