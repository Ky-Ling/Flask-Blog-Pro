from datetime import timedelta
from flask import render_template, flash, redirect, url_for, Blueprint, current_app, request
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.users.forms import UpdateAccountForm
from flaskblog.users.utils import save_picture

users = Blueprint("users", __name__)

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Great", category="success")
        return redirect(url_for("users.account"))
    else:
        if request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email
    
    image_file = url_for("static", file_name="profile_pics/" + current_user.image_file)

    return render_template("account.html")
    