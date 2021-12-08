'''
Date: 2021-12-04 19:29:22
LastEditors: GC
LastEditTime: 2021-12-05 13:36:17
FilePath: \Flask-Blog-Project2\flaskblog\main\routes.py
'''
from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')
