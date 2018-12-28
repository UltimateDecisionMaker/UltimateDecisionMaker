"""
In this file, we test the app we built. The basic guideline is to have at least 3 tests
for each funtion we have. One for normal case; one for edge case; and one for failed case.
"""

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

def test_register1():
    rv = app.test_client().post('/register', data={'email':'aaa','password':'bbb'},follow_redirects=True)
    assert b"Login to view your history choices, see activities from friends, and more crazy features!" in rv.data

def test_login1():
    rv = app.test_client().post('/login', data={'email':'aaa','password':'bbb'},follow_redirects=True)
    assert b"Now, tell us your choices" in rv.data
