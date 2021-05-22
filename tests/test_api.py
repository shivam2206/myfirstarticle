import io
import json

import pytest

from myfirstarticle.database import db
from myfirstarticle.model import Author, Article
from tests.base import BaseTestCase

API_VERSION = 'v1'


class BaseAPITestCase(BaseTestCase):
    DEFAULT_NAME = 'User1 Some'
    DEFAULT_EMAIL = 'user1@some.com'
    DEFAULT_PASSWORD = '12341234'
    DEFAULT_TITLE = 'Welcome to First Article'
    DEFAULT_SHORT_DESCRIPTION = 'This is my description for preview'
    DEFAULT_LONG_DESCRIPTION = '<h2>Now this is the main content.<br></h2>'

    DEFAULT_URL_LOGIN = f'api/{API_VERSION}/auth/login'
    DEFAULT_URL_AUTHORS = f'api/{API_VERSION}/authors'
    DEFAULT_URL_ARTICLES = f'api/{API_VERSION}/articles'

    def register_user(self, url=DEFAULT_URL_AUTHORS, name=DEFAULT_NAME, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD,
                      **kwargs):
        return self.client.post(
            url,
            json=dict(
                name=name,
                email=email,
                password=password
            ),
            **kwargs
        )

    def login_user(self, url=DEFAULT_URL_LOGIN, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, **kwargs):
        return self.client.post(
            url,
            json=dict(
                email=email,
                password=password
            ),
            **kwargs
        )

    def create_article(self, url=DEFAULT_URL_ARTICLES,
                       title=DEFAULT_TITLE,
                       short_description=DEFAULT_SHORT_DESCRIPTION,
                       long_description=DEFAULT_LONG_DESCRIPTION,
                       auto_register=True,
                       **kwargs):
        if auto_register:
            self.register_user()
        token = self.login_user().json['token']

        return self.post_request(
            url,
            json_data=dict(
                title=title,
                short_description=short_description,
                long_description=long_description
            ),
            token=token,
            **kwargs
        )

    def get_request(self, url, token, json_data=None, **kwargs):
        json_data = json_data or None
        return self.client.get(
            url,
            json=json_data,
            headers={'Authorization': 'Bearer {}'.format(token)},
            **kwargs
        )

    def post_request(self, url, token, json_data, **kwargs):
        return self.client.post(
            url,
            json=json_data,
            headers={'Authorization': 'Bearer {}'.format(token)},
            **kwargs
        )

    def put_request(self, url, token, json_data, **kwargs):
        return self.client.put(
            url,
            json=json_data,
            headers={'Authorization': 'Bearer {}'.format(token)},
            **kwargs
        )

    def delete_request(self, url, token, json_data, **kwargs):
        return self.client.delete(
            url,
            json=json_data,
            headers={'Authorization': 'Bearer {}'.format(token)},
            **kwargs
        )


class TestAPIAuthorRoute(BaseAPITestCase):

    def test_successful_registration(self):
        response = self.register_user()
        assert response.status_code == 201
        assert response.json['id'] == 1
        assert response.json['name'] == self.DEFAULT_NAME
        assert response.json['email'] == self.DEFAULT_EMAIL
        assert len(response.json) == 3

        author = Author.query.first()
        assert author is not None
        assert author.id == 1
        assert author.name == self.DEFAULT_NAME
        assert author.email == self.DEFAULT_EMAIL
        assert author.verify_password(self.DEFAULT_PASSWORD)
        assert author.active
        assert author.verified

    def test_same_user_registration(self):
        self.register_user()
        response = self.register_user()
        db.session.rollback()
        items = Author.query.all()
        assert len(items) == 1
        assert response.status_code == 406
        assert response.json['message'] == 'Account already exists'

    def test_invalid_input_user_registration(self):
        response = self.register_user(password='1')
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 422
        assert response.json['messages']['password'][0] == 'Length must be between 4 and 16.'

        response = self.register_user(password='1asdd234234234sdfsdfs3423423sdfsdf')
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 422
        assert response.json['messages']['password'][0] == 'Length must be between 4 and 16.'

        response = self.register_user(email='1')
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 422
        assert response.json['messages']['email'][0] == 'Length must be between 2 and 100.'

        response = self.register_user(name='')
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 422
        assert response.json['messages']['name'][0] == 'Length must be between 1 and 100.'

    def test_author_update(self):
        self.register_user()
        token = self.login_user().json['token']

        data = dict()
        response = self.put_request(self.DEFAULT_URL_AUTHORS, token, json_data=data)
        print(response.json)
        assert response.status_code == 200

        data = dict(name='New name')
        response = self.put_request(self.DEFAULT_URL_AUTHORS, token, json_data=data)
        assert response.status_code == 200
        assert response.json['name'] == data['name']
        assert response.json['email'] == self.DEFAULT_EMAIL
        assert response.json['id'] == 1

        data = dict(password='MyNewPass')
        response = self.put_request(self.DEFAULT_URL_AUTHORS, token, json_data=data)
        assert response.status_code == 200

        author = Author.query.first()
        assert author
        assert author.verify_password(data['password'])


class TestAPIAuthRoute(BaseAPITestCase):
    def test_successful_login(self):
        self.register_user()
        response = self.login_user()
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['token']
        assert len(response.json['token'].split('.')) == 3
        assert len(response.json) == 2

    def test_unsuccessful_login(self):
        self.register_user()
        response = self.login_user(password='121212112')
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'
        assert response.json['status'] == 'failed'

        response = self.login_user(email='ee@ee.ee')
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'

        response = self.login_user(password='')
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'

        response = self.login_user(email='')
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'

        response = self.login_user(email='', password='')
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'


class TestAPIArticleRoute(BaseAPITestCase):

    def test_article_post(self):
        response = self.create_article()
        assert response.status_code == 201
        assert response.json['id'] == 1
        assert response.json['title'] == self.DEFAULT_TITLE
        assert response.json['short_description'] == self.DEFAULT_SHORT_DESCRIPTION
        assert response.json['long_description'] == self.DEFAULT_LONG_DESCRIPTION
        assert response.json['author']['email'] == self.DEFAULT_EMAIL
        assert response.json['author']['name'] == self.DEFAULT_NAME
        assert response.json['author']['id'] == 1

        assert len(Article.query.all()) == 1
        article = Article.query.first()
        assert article
        assert article.title == self.DEFAULT_TITLE
        assert article.short_description == self.DEFAULT_SHORT_DESCRIPTION
        assert article.long_description == self.DEFAULT_LONG_DESCRIPTION
        assert not article.published

    def test_article_get(self):
        self.create_article()

        response = self.client.get(f'api/{API_VERSION}/articles', None)
        assert response.status_code == 403
        assert response.json['message'] == 'Auth token is required to access this resource.'

        response = self.get_request(f'api/{API_VERSION}/articles', None)
        assert response.status_code == 403
        assert response.json['message'] == 'Invalid token. Please log in again.'

        token = self.login_user().json['token']
        response = self.get_request(f'api/{API_VERSION}/articles', token)
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert not response.json['has_next']
        assert not response.json['has_previous']
        assert len(response.json['results']) == 1
        assert response.json['results'][0]['title'] == self.DEFAULT_TITLE
        assert response.json['results'][0]['short_description'] == self.DEFAULT_SHORT_DESCRIPTION
        assert response.json['results'][0]['long_description'] == self.DEFAULT_LONG_DESCRIPTION
        assert response.json['results'][0]['id'] == 1
        assert response.json['results'][0]['author']['email'] == self.DEFAULT_EMAIL
        assert response.json['results'][0]['author']['name'] == self.DEFAULT_NAME
        assert response.json['results'][0]['author']['id'] == 1

    def test_article_pagination(self):
        self.create_article()
        for i in range(3):
            self.create_article(title=f'Another one {i}', auto_register=False)

        token = self.login_user().json['token']
        response = self.get_request(f'api/{API_VERSION}/articles', token)
        assert response.status_code == 200
        assert response.json['count'] == 4
        assert response.json['has_next']
        assert not response.json['has_previous']
        assert len(response.json['results']) == 2

        response = self.get_request(f'api/{API_VERSION}/articles?start=4', token)
        assert response.status_code == 200
        assert response.json['count'] == 4
        assert not response.json['has_next']
        assert response.json['has_previous']
        assert len(response.json['results']) == 1

    def test_article_put(self):
        response = self.create_article()
        article_id = response.json['id']
        data = dict()
        token = self.login_user().json['token']
        response = self.put_request(self.DEFAULT_URL_ARTICLES, token, json_data=data)
        assert response.status_code == 422
        assert response.json['messages']['id'][0] == 'Missing data for required field.'

        data = dict(id=article_id, title='Updated title')
        response = self.put_request(self.DEFAULT_URL_ARTICLES, token, json_data=data)
        assert response.status_code == 200
        assert response.json['id'] == article_id
        assert response.json['title'] == data['title']
        assert response.json['short_description'] == self.DEFAULT_SHORT_DESCRIPTION
        assert response.json['long_description'] == self.DEFAULT_LONG_DESCRIPTION
        assert response.json['author']['email'] == self.DEFAULT_EMAIL
        assert response.json['author']['name'] == self.DEFAULT_NAME
        assert response.json['author']['id'] == 1

        assert len(Article.query.all()) == 1
        article = Article.query.first()
        assert article
        assert article.title == data['title']
        assert article.short_description == self.DEFAULT_SHORT_DESCRIPTION
        assert article.long_description == self.DEFAULT_LONG_DESCRIPTION
        assert not article.published

    def test_article_delete(self):
        response = self.create_article()
        article_id = response.json['id']
        data = dict()
        token = self.login_user().json['token']
        response = self.delete_request(self.DEFAULT_URL_ARTICLES, token, json_data=data)
        assert response.status_code == 422
        assert response.json['messages']['id'][0] == 'Missing data for required field.'

        data = dict(id=article_id)
        response = self.delete_request(self.DEFAULT_URL_ARTICLES, token, json_data=data)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert len(Article.query.all()) == 0
