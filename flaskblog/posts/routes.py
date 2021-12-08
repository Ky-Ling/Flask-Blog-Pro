'''
Date: 2021-12-04 19:29:51
LastEditors: GC
LastEditTime: 2021-12-05 14:23:16
FilePath: \Flask-Blog-Project2\flaskblog\posts\routes.py
'''
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@login_required
@posts.route("/post/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash("Your post has been created!", category="success")
        return redirect(url_for('main.home'))

    return render_template("create_post.html", title='New Post', form=form, legend="New Post")


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Make sure that only the user who wrote this post can update it
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", category="success")

        return redirect(url_for("posts.post", post_id=post.id))

    elif request.method == "GET":
        # Populate these form fields with our current post data
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", category="success")

    return redirect(url_for("main.home"))
