from flask import Blueprint, render_template

home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
def index():
    return render_template('home/home.html')


@home.route('/about')
def about():
    return render_template('home/about.html')
