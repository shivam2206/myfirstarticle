from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from ...database import db
from ...model import Author
from ...schemas import (SuccessSchema,
                        BaseRemoveSchema,
                        AuthorPaginationSchema,
                        AuthorSchema,
                        AuthorUpdateSchema)
from ...utils.decorators import add_pagination, login_required

__all__ = ['AuthorAPI']


@doc(tags=['Authors'])
class AuthorAPI(MethodResource, Resource):
    @login_required
    @marshal_with(AuthorPaginationSchema)
    @add_pagination
    def get(self, **kwargs):

        items = Author.query.all()
        return items

    @use_kwargs(AuthorSchema, location="json")
    @marshal_with(AuthorSchema)
    def post(self, **kwargs):
        new = Author(**kwargs)

        # TODO: Add Email verification support
        new.verified = True
        new.active = True

        try:
            db.session.add(new)
            db.session.commit()
        except IntegrityError:
            return abort(406, message="Account already exists")
        db.session.commit()
        return new, 201

    @login_required
    @use_kwargs(AuthorUpdateSchema, location="json")
    @marshal_with(AuthorUpdateSchema)
    def put(self, **kwargs):
        author = Author.query.get_or_404(kwargs['id'], description="Invalid Id")

        for key in Author.Meta.allow_updates:
            if key in kwargs:
                setattr(author, key, kwargs[key])

        db.session.commit()
        return author

    @login_required
    @use_kwargs(BaseRemoveSchema, location="json")
    @marshal_with(SuccessSchema)
    def delete(self, **kwargs):
        author = Author.query.get_or_404(kwargs['id'], description="Invalid Id")
        try:
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            return {"status": "failed", "message": str(e)}
