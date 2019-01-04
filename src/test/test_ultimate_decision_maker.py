"""Tests for the Ultimate Decision Maker."""


def test_post_from_home_route(app):
    """Test posting from the home route without redirection."""
    app.test_client().post('/', data={
        "submit-button": 'decide-for-me',
        "choice_1": 'burger',
        "choice_2": 'pizza',
    })


def test_home_route_get(app):
    """Test a get to the home route."""
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'Let\'s make some decisions!' in rv.data


def test_home_input(app):
    """Test posting to the home route with redirects."""
    rv = app.test_client().post('/', data={
        'submit-button': 'decide-for-me',
        'choice_1': 'burger',
        'choice_2': 'pizza'},
        follow_redirects=True)

    assert b"DECISION MADE:" in rv.data
    assert (b'burger' in rv.data) or (b'pizza' in rv.data)


def test_bad_route(app):
    """Test an invalid route."""
    rv = app.test_client().get('/foo')
    assert rv.status_code == 404


class TestAuthentication:
    """Test authentication and login gating."""

    def test_registration_redirect_to_login(self, client):
        """Test the registration redirect."""
        rv = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert b"Login here:" in rv.data

    def test_registration_no_same_email(self, client):
        """Test that registration fails if the account already exists."""
        client.post(
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
        """Test that a registered user can successfully login."""
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
        """Test that a registered user can't login with a bad password."""
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
        assert b'Invalid email or password' in rv.data

    def test_registered_user_vision_route(self, authenticated_client):
        """Test the vision route for a logged in user."""
        rv = authenticated_client.get('/vision')
        assert rv.status_code == 200
        assert b'<h1>Upload new File</h1>' in rv.data

    def test_unauthenticated_user_authenticated_route(self, app):
        """Test the vision route if the user is not logged in."""
        res = app.test_client().get('/vision', follow_redirects=True)
        assert b'Please login first.' in res.data

    def test_user_history_route(self, authenticated_client):
        authenticated_client.post('/', data={
            'choice_1': 'burger',
            'choice_2': 'pizza',
            'submit-button': 'decide-for-me'})

        authenticated_client.post('/', data={
            'choice_1': 'burger',
            'choice_2': 'pizza',
            'submit-button': 'go-with-it'})

        rv = authenticated_client.get('/history')
        assert (b'you considered burger, pizza. Ultimately, you chose pizza' in rv.data) or \
            (b'you considered burger, pizza. Ultimately, you chose burger' in rv.data)
