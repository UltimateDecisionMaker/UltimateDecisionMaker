import pytest
from .. import app as _app
from ..models import db as _db
from ..models import Account, Decision, History
import os


@pytest.fixture()
def app(request):
    """Session-wide Testable Flask Application
    """
    _app.config.from_mapping(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):
    """
    """
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def client(app, db, session):
    client = app.test_client()
    ctx = app.app_context()

    ctx.push()

    yield client
    ctx.pop()


@pytest.fixture()
def user(session):
    account = Account(email='test@test.com', password='1234')

    session.add(account)
    session.commit()
    return account


@pytest.fixture()
def authenticated_client(client, user):
    client.post(
        '/login',
        data={'email': user.email, 'password': '1234'},
        follow_redirects=True,
    )
    yield client

    client.get('/logout')
