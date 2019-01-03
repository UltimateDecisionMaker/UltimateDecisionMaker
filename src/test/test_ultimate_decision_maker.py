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
    assert b'Let\'s make some decisions!' in rv.data


def test_home_input(app):
    """
    """
    rv = app.test_client().post('/', data={'submit-button': 'decide-for-me', 'choice_1': 'burger', 'choice_2': 'pizza'}, follow_redirects=True)

    assert b"DECISION MADE:" in rv.data
    assert (b'burger' in rv.data) or (b'pizza' in rv.data)


# def test_register1():
#     rv = app.test_client().post('/register', data={'email': 'aaa', 'password': 'bbb'}, follow_redirects=True)
#     assert b"Login here:" in rv.data


# def test_login1():
#     rv = app.test_client().post('/login', data={'email': 'aaa', 'password': 'bbb'}, follow_redirects=True)
#     assert b"What are you trying to decide between?" in rv.data


class TestAuthentication:

    def test_registration_redirect_to_login(self, client):
        """
        """
        rv = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        # import pdb; pdb.set_trace()
        assert b"Login here:" in rv.data

    def test_registration_no_same_email(self, client):
        tmp = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )

        rv = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'another'},
            follow_redirects=True,
        )
        assert b'test@example.com has already been registered.\n' in rv.data

    def test_registered_user_can_login(self, client):
        client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )

        rv = client.post(
            '/login',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert rv.status_code == 200
        assert b'Let\'s make some decisions!' in rv.data

    def test_registered_user_bad_login(self, client):
        client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )

        rv = client.post(
            '/login',
            data={'email': 'test@example.com', 'password': 'another'},
            follow_redirects=True,
        )
        assert rv.status_code == 200
        # import pdb; pdb.set_trace()
        assert b'Invalid email or password' in rv.data
