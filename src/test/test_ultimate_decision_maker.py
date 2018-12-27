import pytest
from .. import app
from flask import request
from werkzeug import ImmutableMultiDict


def input_for_test(app):
    app.post('/', data=dict(
        choice1='burger',
        choice2='pizza'
    ))


def test_imports():
    """
    test import app is successful.
    """
    assert app

def test_home():
    """
    """
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'Welcome to the Ultimate Decision Maker.' in rv.data

def test_home_input(app):
    """
    """
    rv = app.test_client().post('/', data={'choice1':'burger','choice2':'pizza'},follow_redirects=True)

    assert b"Here's what you shall go along with!" in rv.data
    assert (b'burger' in rv.data) or (b'pizza' in rv.data)
