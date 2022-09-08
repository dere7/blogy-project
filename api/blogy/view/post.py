'''post view'''
from datetime import datetime as dt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from .use_form import use_form
from ..forms.post_form import (
    CreatePostForm,
    CommentForm,
    UpdatePostForm
)
from ..models.post import Post

bp = Blueprint('post', __name__)


def get_posts_paginated(**query):
    '''returns paginated posts'''
    posts = Post.objects(**query).paginate(
        page=int(request.args.get('page') or 1),
        per_page=int(request.args.get('limit') or 1),
    )
    return jsonify(
        posts=[post.to_dict() for post in posts.items],
        page=posts.page,
        pages=posts.pages,
        has_prev=posts.has_prev,
        has_next=posts.has_next
    )


@bp.route('/')
def get_posts():
    """
    GET /
        - get posts
    """
    return get_posts_paginated()


@bp.route('/me/posts')
@jwt_required()
def get_user_posts():
    """
    GET /me/posts
        - get current user posts
    """
    return get_posts_paginated(author=current_user)


@bp.route('/', methods=['POST'])
@jwt_required()
@use_form(CreatePostForm)
def create_post(form):
    """
    POST /
        - create new post
    """
    post = Post(**form.data, author=current_user).save()
    return post.to_dict(), 201


@bp.route('/<slug>')
def get_post(slug):
    """
    GET /<slug>
        - get post
    """
    post = Post.objects(slug=slug).first_or_404()
    return post.to_dict()


@bp.route('/<slug>', methods=['PUT'])
@jwt_required()
@use_form(UpdatePostForm)
def update_post(form, slug):
    """
    PUT /<slug>
        - update post
    """
    post = Post.objects(slug=slug).first_or_404()
    if post.author != current_user:
        return jsonify(error='The post doesn\'t belong to you'), 401
    post.updated_at = dt.utcnow()
    for field, value in request.json.items():
        if field in form.data:
            setattr(post, field, value)
    post.save(validate=False)
    return post.to_dict()


@bp.route('/<slug>', methods=['DELETE'])
@jwt_required()
def delete_post(slug):
    """
    DELETE /<slug>
        - delete post
    """
    post = Post.objects(slug=slug).first_or_404()
    post.delete()
    return jsonify(msg='Successfully deleted.')


@bp.route('/<slug>/publish', methods=['PUT'])
@jwt_required()
def publish_post(slug):
    """
    PUT /<slug>/publish
        - publish post
    """
    post = Post.objects(slug=slug).first_or_404()
    post.is_published = True
    post.published_at = dt.utcnow()
    post.save()
    return post.to_dict()


@bp.route('/<slug>/unpublish', methods=['PUT'])
@jwt_required()
def unpublish_post(slug):
    """
    PUT /<slug>/unpublish
        - unpublish post
    """
    post = Post.objects(slug=slug).first_or_404()
    post.is_published = False
    post.published_at = None
    post.save()
    return post.to_dict()


@bp.route('/<slug>/comment', methods=['POST'])
@jwt_required()
@use_form(CommentForm)
def comment(form, slug):
    """
    POST /<slug>/comment
        - comment post
    """
    post = Post.objects(slug=slug).first_or_404()
    post.comments.create(content=form.data['content'], user=current_user)
    post.save()
    return post.to_dict()


@bp.route('/<slug>/comment', methods=['GET'])
def get_comments(slug):
    """
    GET /<slug>/comment
        - get comments
    """
    post = Post.objects(slug=slug).first_or_404()
    return post.comments
