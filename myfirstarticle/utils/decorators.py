from flask import request
from flask_restful import abort

from .helper import decode_auth_token
from .paginator import get_paginated_list
from functools import wraps

from ..model import Author
from ..settings import MAX_PAGE_ITEMS


def add_pagination(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(request.args)
        result = get_paginated_list(func(*args, **kwargs), request.args.get('start', 1), MAX_PAGE_ITEMS)
        return result
    return decorated


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split()[1] if len(auth_header.split()) > 1 else ''
            else:
                auth_token = ''
            if auth_token:
                user_id = decode_auth_token(auth_token)
                author = Author.query.filter_by(id=user_id).first()
                if not author or not (author.active and author.verified):
                    raise Exception("This account is not allowed to access this resource.")
                kwargs['author'] = author

            else:
                raise Exception("Auth token is required to access this resource.")
        except Exception as e:
            abort(403, message=str(e))
        result = func(*args, **kwargs)
        return result
    return decorated
