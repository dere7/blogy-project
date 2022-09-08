'''use_form decorator'''
import functools
from flask import jsonify


def use_form(form_class):
    '''decorator to validate post and return 400 if form is invalid'''
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            form = form_class()
            if not form.validate():
                return jsonify(error=form.errors), 400
            return view(form, *args, **kwargs)
        return wrapper
    return decorator
