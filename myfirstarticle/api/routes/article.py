import json

from flask_apispec import marshal_with
from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from ...model import Article
from ...schemas.article import ArticlePaginationSchema
from ...utils.decorators import add_pagination


class ArticleAPI(MethodResource, Resource):
    @marshal_with(ArticlePaginationSchema)
    @add_pagination
    def get(self):
        articles = Article.query.all()
        return articles
