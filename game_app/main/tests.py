import os 
import unittest

from game_app import app, db, bcrypt
from game_app.models import User, System, Game


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='user', password=password_hash)
    db.session.add(user)
    db.session.commit()


# Tests

class MainTests(unittest.TestCase):

    def setUp(self):
       
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Log Out', response_text)

    def test_homepage_logged_in(self):
        # Set up
        create_user()
        login(self.app, 'user', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Log Out', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_system(self):

        # Set up
        create_user()
        login(self.app, 'user', 'password')

        # POST request with test data
        post_data = {
            'name': 'system',
            'purchased': '01/01/2020'
        }
        self.app.post('/new_system', data=post_data)

        system = System.query.filter_by(name='system').first()
        self.assertIsNotNone(system)
        self.assertEqual(system.name, 'system')
    
    def test_system_logged_out(self):

        response = self.app.get('/new_system')

        self.assertEqual(response.status_code, 302)