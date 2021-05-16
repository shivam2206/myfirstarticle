from flask import Blueprint, render_template
from werkzeug.utils import redirect

from myfirstarticle.model import Article

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
