from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config=True
)

from . import routes, exceptions
