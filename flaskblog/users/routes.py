from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, sent_reset_email
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Create an instance of our form that we are going to send to our userslication
    form = RegistrationForm()

    # Check if our form validated when it was submitted
    if form.validate_on_submit():
        # Authentication:
        # hashed_password = bcrypt.generate_password_hash(
        #     form.password.data).decode('utf-8')

        # # Create a new instance of a user:
        # user = User(username=form.username.data,
        #             email=form.email.data, password=hashed_password)
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(
            form.password.data, method="sha256"))
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=form.password.data)
        flash('Your account has been created! Enjoy this funny blog website!',
              category="success")
        return redirect(url_for("main.home"))

    return render_template("register.html", title="registration", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Simultaneously check whether the user exists and their password verifies with what they have in the database
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and check_password_hash(user.password, form.password.data):
            # Log the user in:
            login_user(user, remember=form.remember.data)

            # Get the next parameter from the URL
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash(
                "Login unsuccessful. Please checkout email and password", category="danger")

    return render_template("login.html", title="login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_required
# Put a check in place that makes a user login before they can access this account page
@users.route("/account", methods=["GET", "POST"])
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            # Save the profile picture for the user
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Update the current username and email
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", category="success")
        return redirect(url_for("users.account"))

    else:
        if request.method == "GET":
            # Populate these form fields with our current user data
            form.username.data = current_user.username
            form.email.data = current_user.email

    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=2)

    return render_template("user_posts.html", posts=posts, user=user)


# Put in the email for us to send that information and we wanna the user to be logged out in order to get this page.
@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect("home")

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Send this user and email with their token that they can reset their password
        sent_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info")

        return redirect(url_for("users.login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token.", category="warning")

        return redirect(url_for("users.reset_request"))

    # Display the form for the user to update their password
    form = ResetPasswordForm()

    # Handle the form submission when they actually changed the password.
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()

        flash('Your password has been updated! You are now able to log in.',
              category="success")
        return redirect(url_for("users.login"))

    return render_template("reset_token.html", title="Reset Password", form=form)
