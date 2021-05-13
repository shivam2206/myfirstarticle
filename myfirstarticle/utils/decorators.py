from .paginator import get_paginated_list
from functools import wraps

from ..settings import MAX_PAGE_ITEMS


def add_pagination(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        result = get_paginated_list(func(*args, **kwargs), 1, MAX_PAGE_ITEMS)
        return result
    return decorated
