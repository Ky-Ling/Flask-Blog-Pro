'''
Date: 2021-12-05 16:08:09
LastEditors: GC
LastEditTime: 2021-12-05 16:12:32
FilePath: \Flask-Blog-Project2\flaskblog\errors\handler.py
'''
from flask import Blueprint, render_template
errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500
