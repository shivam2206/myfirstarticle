from flask import Blueprint, render_template

from myfirstarticle.model import Article

home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
def index():
    items = Article.query.order_by(Article.created_on.desc()).limit(10).all()
    return render_template('home/home.html', items=items)


@home.route('/about')
def about():
    return render_template('home/about.html')
