import json

from flask import request
from flask_apispec import marshal_with
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import ValidationError

from ...model import Article
from ...schemas.article import ArticlePaginationSchema, ArticleSchema, ArticleUpdateSchema
from ...schemas.base import SuccessSchema, BaseRemoveSchema
from ...utils.decorators import add_pagination
from ...database import db


class ArticleAPI(MethodResource, Resource):
    @marshal_with(ArticlePaginationSchema)
    @add_pagination
    def get(self):
        articles = Article.query.all()
        return articles

    @use_kwargs(ArticleSchema, location="json")
    @marshal_with(ArticleSchema)
    def post(self, **kwargs):
        new = Article(**kwargs)
        db.session.add(new)
        db.session.commit()
        return new

    @use_kwargs(ArticleUpdateSchema, location="json")
    @marshal_with(ArticleUpdateSchema)
    def put(self, **kwargs):
        article = Article.query.get_or_404(kwargs['id'], description="Invalid Id")

        for key in Article.Meta.allow_updates:
            if key in kwargs:
                setattr(article, key, kwargs[key])

        db.session.commit()
        return article

    @use_kwargs(BaseRemoveSchema, location="json")
    @marshal_with(SuccessSchema)
    def delete(self, **kwargs):
        article = Article.query.get_or_404(kwargs['id'], description="Invalid Id")
        try:
            db.session.delete(article)
        except Exception as e:
            return {"status": "failed", "message": str(e)}
