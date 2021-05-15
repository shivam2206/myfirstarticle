from .author import *
from .article import *
from .auth import *

tags = [
    {'name': 'Articles',
     'description': 'For all Article related operations'
     },
    {'name': 'Authors',
     'description': 'For all Author related operations'
     },
    {'name': 'Auth',
     'description': 'For authentication'
     },
]


def initialize_routes(api, docs):
    def add_route(resource, route):
        api.add_resource(resource, route)
        docs.register(resource)

    add_route(ArticleAPI, '/articles')
    add_route(AuthorAPI, '/authors')
    add_route(AuthLoginAPI, '/auth/login')

    for tag in tags:
        docs.spec.tag(tag)

