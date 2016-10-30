# coding: utf-8

import os
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'


from . import views

# Register Blueprint
# from auth import auth
# app.register_blueprint(auth, url_prefix='/auth')