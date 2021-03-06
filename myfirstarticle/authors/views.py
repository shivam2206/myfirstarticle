import traceback

from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect

from myfirstarticle.database import db
from myfirstarticle.model import Author, Article
from myfirstarticle.schemas import AuthorSchema, AuthSchema

authors = Blueprint('authors',
                    __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/')


@authors.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    status_code = 200
    if request.method == 'POST':
        try:
            validated_data = AuthorSchema().load(request.form)
            new = Author(**validated_data)

            # TODO: Add verification support
            new.verified = True
            new.active = True

            db.session.add(new)
            db.session.commit()
            flash('Account has been created successfully, please login to access', 'success')
            return redirect(url_for('authors.login'))
        except ValidationError as e:
            errors = e.normalized_messages()
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
            status_code = 400
        except IntegrityError:
            flash('This Account already exists, please login', 'error')
            status_code = 422
        except Exception as e:
            status_code = 400
            flash('Unknown error occurred', 'error')
    return render_template('authors/register.html'), status_code


@authors.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    status_code = 200
    if request.method == 'POST':
        try:
            validated_data = AuthSchema().load(request.form)
            author = Author.query.filter_by(email=validated_data['email']).first()
            if not author or not author.verify_password(validated_data['password']):
                raise ValidationError("Invalid username or password.")
            if not (author.active and author.verified):
                raise ValidationError("This account is not active.")
            login_user(author)
            next_url = request.args.get('next')
            return redirect(next_url or '/')

        except ValidationError as e:
            if isinstance(e, str):
                flash(e, 'error')
            errors = e.normalized_messages()
            status_code = 401
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
        except Exception as e:
            print(e)
            traceback.print_exc()
            flash('Unknown error occurred', 'error')
            status_code = 401
    return render_template('authors/login.html'), status_code


@authors.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@authors.route("/profile/<int:author_id>")
@login_required
def profile(author_id):
    author = Author.query.get_or_404(author_id)
    items = Article.query.filter_by(author_id=author.id).order_by(Article.created_on.desc()).all()
    return render_template('authors/profile_view.html', author=author, items=items, hide_posted_by=True)


@authors.route("/create")
@login_required
def create():
    return "Here you go!!"
