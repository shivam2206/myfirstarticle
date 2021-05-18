import time

from sqlalchemy.exc import IntegrityError

from myfirstarticle.database import db
from myfirstarticle.model import Author, Article
from tests.base import BaseTestCase


class BaseModel(BaseTestCase):
    MODEL = None

    def test_obj(self):
        if self.MODEL is not None:
            raise NotImplementedError

    def test_ensure_model_meta(self):
        if self.MODEL is not None:
            assert hasattr(self.MODEL, 'Meta')
            assert hasattr(self.MODEL.Meta, 'allow_updates')


class TestAuthorModel(BaseModel):
    MODEL = Author

    @staticmethod
    def create_author():
        author = Author(
            name='Sample User',
            email='user@sample.com',
            password='test123411'
        )
        db.session.add(author)
        db.session.commit()
        author = Author.query.first()
        return author

    def test_obj(self):
        obj = self.create_author()
        assert obj.name == 'Sample User'
        assert obj.email == 'user@sample.com'
        assert not obj.active
        assert not obj.verified
        assert len(obj.articles) == 0

    def test_with_article(self):
        article = Article(
            title='Article on test cases',
            short_description='Here goes my short description',
            long_description='This is the main content'
        )
        obj = self.create_author()
        article.author_id = obj.id
        db.session.add(article)
        db.session.commit()

        retrieved = Author.query.first()
        assert len(retrieved.articles) == 1
        assert isinstance(retrieved.articles[0], Article)
        assert retrieved.articles[0].id == 1

    def test_verify_password(self):
        author = self.create_author()
        assert not author.verify_password('invalid_password')
        assert author.verify_password('test123411')

    def test_password_readability(self):
        author = self.create_author()
        with self.assertRaises(AttributeError) as ae:
            password = author.password
        assert str(ae.exception) == 'Can\'t read password'

    def test_is_active(self):
        author = self.create_author()
        assert not author.is_active()

        author.active = True
        assert not author.is_active()

        author.active = False
        author.verified = True
        assert not author.is_active()

        author.active = True
        author.verified = True
        assert author.is_active()

    def test_get_id(self):
        author = self.create_author()
        assert author.get_id() == author.id

    def test_updatable_fields(self):
        assert Author.Meta.allow_updates == ['name', 'active', 'password', 'verified']

    def test_str_formatting(self):
        author = self.create_author()
        assert str(author) == '<Author id=1 name=Sample User>'


class TestArticleModel(BaseModel):
    MODEL = Article

    @staticmethod
    def create_article(commit=True):
        article = Article(
            title='Article on test cases',
            short_description='Here goes my short description',
            long_description='This is the main content'
        )
        if commit:
            db.session.add(article)
            db.session.commit()
            article = Article.query.first()
        return article

    def test_obj(self):
        obj = self.create_article()
        assert obj.title == 'Article on test cases'
        assert obj.short_description == 'Here goes my short description'
        assert obj.long_description == 'This is the main content'
        assert not obj.published
        assert obj.author_id is None
        assert obj.author is None

    def test_with_author(self):
        obj = self.create_article(commit=False)
        author = Author(
            name='Sample User',
            email='user@sample.com',
            password='test123411'
        )
        db.session.add(author)
        db.session.commit()
        obj.author_id = author.id
        db.session.add(obj)
        db.session.commit()
        obj = Article.query.first()
        assert obj.title == 'Article on test cases'
        assert obj.short_description == 'Here goes my short description'
        assert obj.long_description == 'This is the main content'
        assert not obj.published
        assert obj.author_id == 1
        assert isinstance(obj.author, Author)
        assert obj.author.id == 1

    def test_modified_time(self):
        obj = self.create_article()
        time.sleep(1)
        obj.published = True
        db.session.commit()
        obj = Article.query.first()
        assert not obj.modified_on == obj.created_on

    def test_updatable_fields(self):
        assert Article.Meta.allow_updates == ['title', 'short_description', 'long_description', 'published']

    def test_str_formatting(self):
        obj = self.create_article()
        assert str(obj) == '<Article id=1 title=Article on test cases>'

    def test_constraints(self):
        article = Article(
            title=None,
            short_description='Here goes my short description',
            long_description='This is the main content'
        )
        with self.assertRaises(IntegrityError) as ie:
            db.session.add(article)
            db.session.commit()
        db.session.rollback()

        article = Article(
            title='Good title',
            short_description=None,
            long_description='This is the main content'
        )
        with self.assertRaises(IntegrityError) as ie:
            db.session.add(article)
            db.session.commit()
        db.session.rollback()
        article = Article(
            title='Good title',
            short_description='I am here now',
            long_description=None
        )
        with self.assertRaises(IntegrityError) as ie:
            db.session.add(article)
            db.session.commit()
