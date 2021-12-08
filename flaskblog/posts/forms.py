'''
Date: 2021-12-04 19:30:28
LastEditors: GC
LastEditTime: 2021-12-05 13:37:09
FilePath: \Flask-Blog-Project2\flaskblog\posts\forms.py
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
