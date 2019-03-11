import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# create flask app
app = Flask(__name__)

# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/xnuccalc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# set secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# add use of zip()
app.jinja_env.globals.update(zip=zip)
app.jinja_env.globals.update(len=len)

# Install Bootstrap extension
Bootstrap(app)

# create database
db = SQLAlchemy(app)
db.create_all()

from app import routes