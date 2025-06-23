import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from enhanced_blog.flaskblog import create_app, db
from enhanced_blog.flaskblog.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    res = client.get('/')
    assert res.status_code == 200


def test_user_registration(client, app):
    res = client.post('/auth/register', data={
        'username': 'tester',
        'email': 'tester@example.com',
        'password': 'pass',
        'confirm_password': 'pass'
    }, follow_redirects=True)
    assert b'Account created' in res.data
    with app.app_context():
        assert User.query.filter_by(username='tester').first() is not None
