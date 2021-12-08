import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from werkzeug.utils import secure_filename


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    # Grab the file extension from the file that they uploaded.
    _, f_ext = os.path.splitext(form_picture.filename)

    # Combine the random hex with the file extension in order to get the file name of the image that we are going to save.
    picture_fn = secure_filename(random_hex + f_ext)

    # root_path: give us the route path of our application all the way up to our package directory
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize this picture to 125 pixels before we save it
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save the users uploaded image to the file system
    i.save(picture_path)

    return picture_fn


def sent_reset_email(user):

    # Send the user and email with the reset token
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@demo.com", recipients=[user.email])

    msg.body = f'''To reset your password, please visit the following link:
{ url_for("users.reset_token", token=token, _external=True) }
If you did not make this request then simply ignore this email and no changes will be made.
'''
    # mail = mail_configuration(app=app)
    mail.send(msg)
