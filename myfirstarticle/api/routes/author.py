from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from ...database import db
from ...model import Author
from ...schemas import (AuthorSchema,
                        AuthorUpdateSchema, SuccessSchema)
from ...utils.decorators import login_required

__all__ = ['AuthorAPI']


@doc(tags=['Authors'])
class AuthorAPI(MethodResource, Resource):

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
    @marshal_with(AuthorSchema)
    def put(self, **kwargs):
        author = kwargs['author']

        for key in Author.Meta.allow_updates:
            if key in kwargs:
                setattr(author, key, kwargs[key])

        db.session.commit()
        return author
