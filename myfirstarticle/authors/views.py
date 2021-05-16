import traceback

from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect

from myfirstarticle.database import db
from myfirstarticle.model import Author
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
            return redirect('/register')
        except ValidationError as e:
            errors = e.normalized_messages()
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
        except IntegrityError:
            flash('This Account already exists, please login', 'error')
        except Exception as e:
            print(e)
            flash('Unknown error occurred', 'error')
    return render_template('authors/register.html')


@authors.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        try:
            validated_data = AuthSchema().load(request.form)
            author = Author.query.filter_by(email=validated_data['email']).first()
            if not author or not author.verify_password(validated_data['password']):
                raise ValidationError("Invalid username or password")
            if not (author.active and author.verified):
                raise ValidationError("This account is not active")
            login_user(author)
            next_url = request.args.get('next')
            print("Redirecting to ", next_url)
            return redirect(next_url or '/')

        except ValidationError as e:
            if isinstance(e, str):
                flash(e, 'error')
            errors = e.normalized_messages()
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
        except IntegrityError:
            flash('This Account already exists, please login', 'error')
        except Exception as e:
            print(e)
            traceback.print_exc()
            flash('Unknown error occurred', 'error')
    return render_template('authors/login.html')


@authors.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@authors.route("/profile")
@login_required
def profile():
    return "Here you go!!"


@authors.route("/create")
@login_required
def create():
    return "Here you go!!"
