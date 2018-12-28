import pytest
from flask import request
from .. import app as _app
import os


@pytest.fixture()
def app(request):
    """Session-wide Testable Flask Application
    """
    _app.config.from_mapping(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        # SECRET_KEY=os.environ.get('SECRET_KEY'),
        # SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        # SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


# @pytest.fixture()
# def portfolio(session, account):
#     """
#     """
#     portfolio = Portfolio(
#         name='Default',
#         account_id=account.id
#     )

#     session.add(portfolio)
#     session.commit()
#     return portfolio
