import json
import os
from datetime import datetime

from flask import Blueprint, render_template, request, url_for, jsonify, flash, Response
from flask_login import login_required, current_user
from marshmallow import ValidationError
from werkzeug.utils import redirect

from myfirstarticle.database import db
from myfirstarticle.model import Article
from myfirstarticle.schemas import ArticleSchema
from myfirstarticle.settings import ASSETS_UPLOAD_PATH

articles = Blueprint('articles',
                     __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/articles')


@articles.route('/')
def index():
    return redirect('/')


@articles.route('/<int:article_id>')
def view(article_id):
    item = Article.query.get_or_404(article_id)
    return render_template('articles/view.html', item=item)


@articles.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            validated_data = ArticleSchema().load(request.form)
            new = Article(**validated_data)
            new.published = True
            new.author_id = current_user.id
            db.session.add(new)
            db.session.commit()
            flash('Congratulations you just did amazing! Article is live.', 'success')
            return redirect(url_for('articles.view', article_id=new.id))
        except ValidationError as e:
            errors = e.normalized_messages()
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
        except Exception as e:
            print(e)
            flash('Unknown error occurred', 'error')
    return render_template('articles/add.html')


@articles.route('/image_uploader', methods=['POST'])
# @login_required
def image_uploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        filename = f'file_{str(datetime.utcnow())}.{ext}'
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            path = os.path.join(ASSETS_UPLOAD_PATH, filename)
            file.save(path)
            return jsonify({'location': filename})
    output = Response(json.dumps({'status': 'failed',
                                  'message': 'Filename needs to be JPG, JPEG, GIF or PNG'}),
                      status=400,
                      headers={'Error': 'Filename needs to be JPG, JPEG, GIF or PNG'},
                      content_type='application/json')
    # output.headers['Error'] = 'Filename needs to be JPG, JPEG, GIF or PNG'
    return output


@articles.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    item = Article.query.get_or_404(article_id)
    if request.method == 'POST':
        try:
            validated_data = ArticleSchema().load(request.form)
            for key in Article.Meta.allow_updates:
                if key in validated_data:
                    setattr(item, key, request.form[key])
            db.session.commit()
            flash('Article has been updated successfully.', 'success')
            return redirect(url_for('articles.view', article_id=item.id))
        except ValidationError as e:
            errors = e.normalized_messages()
            for key, error in errors.items():
                flash(f'Issue with {key}: {error[0]}', 'error')
        except Exception as e:
            print(e)
            flash('Unknown error occurred', 'error')
    return render_template('articles/edit.html', item=item)


@articles.route('/delete/<int:article_id>', methods=['GET'])
@login_required
def delete(article_id):
    item = Article.query.get_or_404(article_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Article has been removed successfully.', 'success')
        return redirect(url_for('articles.index'))
    except ValidationError as e:
        errors = e.normalized_messages()
        for key, error in errors.items():
            flash(f'Issue with {key}: {error[0]}', 'error')
    except Exception as e:
        print(e)
        flash('Unknown error occurred', 'error')
    return redirect(url_for('articles.index'))
