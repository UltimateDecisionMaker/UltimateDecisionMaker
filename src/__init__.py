import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config=True
)

app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    CACHE_TYPE='simple',
)


from . import auth, models, routes, forms, exceptions
