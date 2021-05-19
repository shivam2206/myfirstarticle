import io
import json
from myfirstarticle.database import db
from myfirstarticle.model import Author, Article
from tests.base import BaseTestCase


class BaseRouteTestCase(BaseTestCase):
    DEFAULT_NAME = 'User1 Some'
    DEFAULT_EMAIL = 'user1@some.com'
    DEFAULT_PASSWORD = '12341234'
    DEFAULT_TITLE = 'Welcome to First Article'
    DEFAULT_SHORT_DESCRIPTION = 'This is my description for preview'
    DEFAULT_LONG_DESCRIPTION = '<h2>Now this is the main content.<br></h2>'

    DEFAULT_URL_LOGIN = '/login'
    DEFAULT_URL_REGISTER = '/register'
    DEFAULT_URL_CREATE_ARTICLE = '/articles/create'

    def register_user(self, url=DEFAULT_URL_REGISTER, name=DEFAULT_NAME, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD,
                      **kwargs):
        return self.client.post(
            url,
            data=dict(
                name=name,
                email=email,
                password=password
            ),
            **kwargs
        )

    def login_user(self, url=DEFAULT_URL_LOGIN, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, **kwargs):
        return self.client.post(
            url,
            data=dict(
                email=email,
                password=password
            ),
            **kwargs
        )

    def create_article(self, url=DEFAULT_URL_CREATE_ARTICLE,
                       title=DEFAULT_TITLE,
                       short_description=DEFAULT_SHORT_DESCRIPTION,
                       long_description=DEFAULT_LONG_DESCRIPTION,
                       auto_login=True,
                       **kwargs):
        if auto_login:
            self.register_user()
            self.login_user()
        return self.client.post(
            url,
            data=dict(
                title=title,
                short_description=short_description,
                long_description=long_description
            ),
            **kwargs
        )


class TestGeneralRoutes(BaseRouteTestCase):

    def test_homepage(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_about_us(self):
        response = self.client.get('/about')
        assert response.status_code == 200

    def test_login(self):
        response = self.client.get('/login')
        assert response.status_code == 200

    def test_register(self):
        response = self.client.get('/register')
        assert response.status_code == 200

    def test_articles_without_id_redirect(self):
        response = self.client.get('/articles/', follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/'

        response = self.client.get('/articles/', follow_redirects=True)
        assert response.status_code == 200

    def test_404(self):
        response = self.client.get('/invalid', follow_redirects=True)
        assert response.status_code == 404


class TestAuthenticationRoutes(BaseRouteTestCase):

    def test_successful_registration(self):
        response = self.register_user(follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/login'

        author = Author.query.first()
        assert author is not None
        assert author.id == 1
        assert author.name == self.DEFAULT_NAME
        assert author.email == self.DEFAULT_EMAIL
        assert author.verify_password(self.DEFAULT_PASSWORD)
        assert author.active
        assert author.verified

    def test_successful_registration_message(self):
        response = self.register_user(follow_redirects=True)
        assert response.status_code == 200
        assert 'Account has been created successfully, please login to access' in response.get_data(as_text=True)

    def test_same_user_registration(self):
        self.register_user(follow_redirects=True)
        response = self.register_user(follow_redirects=True)
        db.session.rollback()
        items = Author.query.all()
        assert len(items) == 1
        assert response.status_code == 422
        assert 'This Account already exists, please login' in response.get_data(as_text=True)

    def test_invalid_input_user_registration(self):
        response = self.register_user(password='1', follow_redirects=True)
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 400
        assert 'Issue with password: Length must be between 4 and 16.' in response.get_data(as_text=True)

        response = self.register_user(password='1asdd234234234sdfsdfs3423423sdfsdf', follow_redirects=True)
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 400
        assert 'Issue with password: Length must be between 4 and 16.' in response.get_data(as_text=True)

        response = self.register_user(email='1', follow_redirects=True)
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 400
        assert 'Issue with email: Length must be between 2 and 100.' in response.get_data(as_text=True)

        response = self.register_user(name='', follow_redirects=True)
        items = Author.query.all()
        assert len(items) == 0
        assert response.status_code == 400
        assert 'Issue with name: Length must be between 1 and 100.' in response.get_data(as_text=True)

    def test_successful_login(self):
        self.register_user()
        response = self.login_user()
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/'

        response = self.client.get('/articles/create')
        assert response.status_code == 200
        assert 'Publish' in response.get_data(as_text=True)

    def test_unsuccessful_login(self):
        self.register_user()
        response = self.login_user(password='121212112')
        assert response.status_code == 401
        assert 'Invalid username or password.' in response.get_data(as_text=True)

        response = self.login_user(email='ee@ee.ee')
        assert response.status_code == 401
        assert 'Invalid username or password.' in response.get_data(as_text=True)

        response = self.login_user(password='')
        assert response.status_code == 401
        assert 'Invalid username or password.' in response.get_data(as_text=True)

        response = self.login_user(email='')
        assert response.status_code == 401
        assert 'Invalid username or password.' in response.get_data(as_text=True)

        response = self.login_user(email='', password='')
        assert response.status_code == 401
        assert 'Invalid username or password.' in response.get_data(as_text=True)

    def test_logout(self):
        self.register_user()
        self.login_user()

        response = self.client.get('/logout')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/'

        response = self.client.get('/articles/create')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/login?next=%2Farticles%2Fcreate'

        response = self.client.get('/articles/create', follow_redirects=True)
        assert response.status_code == 200
        assert 'Please log in to access this page.' in response.get_data(as_text=True)

    def test_successful_login_redirect(self):
        self.register_user()
        response = self.client.get('/articles/create')
        response = self.login_user(url=response.headers['Location'])
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/articles/create'


class TestArticleRoutes(BaseRouteTestCase):

    def test_article_create(self):
        response = self.create_article()
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/articles/1'

        article = Article.query.first()
        assert article
        assert article.title == self.DEFAULT_TITLE
        assert article.short_description == self.DEFAULT_SHORT_DESCRIPTION
        assert article.long_description == self.DEFAULT_LONG_DESCRIPTION
        assert article.published

    def test_article_view(self):
        self.create_article()
        response = self.client.get('/articles/1')
        assert response.status_code == 200
        assert self.DEFAULT_TITLE in response.get_data(as_text=True)
        assert self.DEFAULT_LONG_DESCRIPTION in response.get_data(as_text=True)

    def test_article_on_homepage(self):
        self.create_article()
        response = self.client.get('/')
        assert response.status_code == 200
        assert self.DEFAULT_TITLE in response.get_data(as_text=True)
        assert self.DEFAULT_SHORT_DESCRIPTION in response.get_data(as_text=True)

    def test_article_options(self):
        self.create_article(follow_redirects=True)
        response = self.client.get('/articles/1')
        assert '/articles/edit' in response.get_data(as_text=True)
        assert '/articles/delete' in response.get_data(as_text=True)

        self.client.get('/logout')
        email = 'newuser@new.com'
        password = '43214321'
        self.register_user(email=email, password=password)
        self.login_user(email=email, password=password)

        response = self.client.get('/articles/1')
        assert '/articles/edit' not in response.get_data(as_text=True)
        assert '/articles/delete' not in response.get_data(as_text=True)

    def test_article_edit(self):
        self.create_article()
        data = dict(title='Updated title is here',
                    short_description='I got updated too.',
                    long_description='!!! <b>Awesome content</b> !!!')
        response = self.client.get('/articles/edit/1')
        assert response.status_code == 200
        assert 'Publish' in response.get_data(as_text=True)

        response = self.client.post('/articles/edit/1', data=data)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/articles/1'

        articles = Article.query.all()
        assert len(articles) == 1  # Ensure it didn't create a new entry
        assert articles[0].title == data['title']
        assert articles[0].short_description == data['short_description']
        assert articles[0].long_description == data['long_description']
        assert articles[0].created_on < articles[0].modified_on

        response = self.client.get('/articles/edit/1', follow_redirects=True)
        assert response.status_code == 200
        assert 'Article has been updated successfully.' in response.get_data(as_text=True)

    def test_article_delete(self):
        self.create_article()
        response = self.client.get('/articles/delete/1')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://127.0.0.1:5000/articles/'

        assert not Article.query.first()

    def test_article_delete_message(self):
        self.create_article()
        response = self.client.get('/articles/delete/1', follow_redirects=True)
        assert response.status_code == 200
        assert 'Article has been removed successfully.' in response.get_data(as_text=True)

    def test_invalid_article(self):
        response = self.client.get('articles/345')
        assert response.status_code == 404

    def test_successful_file_upload(self):
        data = dict()
        data['file'] = (io.BytesIO(b"a fake image"), 'fake.jpg')
        self.register_user()
        self.login_user()
        response = self.client.post(
            '/articles/image_uploader', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        file_name = json.loads(response.get_data(as_text=True))['location']
        assert 'file_' in file_name
        assert '.jpg' in file_name

    def test_invalid_file_upload(self):
        data = dict()
        data['file'] = (io.BytesIO(b"a fake file"), 'fake.pdf')
        self.register_user()
        self.login_user()
        response = self.client.post(
            '/articles/image_uploader', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        assert response.headers['Error'] == 'Filename needs to be JPG, JPEG, GIF or PNG'
        assert json.loads(response.get_data(as_text=True))['message'] == 'Filename needs to be JPG, JPEG, GIF or PNG'
