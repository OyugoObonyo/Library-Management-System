"""
A module containing the application's test suite
"""
import os

# use an in memory db for tests above all imports
# ensures that variable is correctly set by the time config file is imported
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from flask import current_app
from app.models import Book, User
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """
    Basetest class that contains the setup and teardown function
    """
    def setUp(self):
        """
        Set up database temporarily
        """
        # create an instance of our app
        self.app = create_app()
        # load up everything we need to create the app
        self.appctx = self.app.app_context()
        # push context to application_context stack
        self.appctx.push()
        db.create_all()
        self.update_user()
        self.update_book()
        # create client to enable app to mock requests during testing
        self.client = self.app.test_client

    def tearDown(self):
        """
        Destroy temporary database
        """
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def update_user(self):
        """
        Method adds a user to the db so as to handle routes where log in is required
        """
        user = User(name="username", email="username@email.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    def update_book(self):
        """
        Method adds a user to the db so as to handle routes where log in is required
        """
        book = Book(title="A book", synopsis="A really good read")
        db.session.add(book)
        db.session.commit()

    def login(self):
        """
        Method that performs log in for user
        """
        with self.client() as c:
            c.post('/auth/login', data={
                "username": "username",
                "password": "password"
            })

    
# unit tests for the user model
class UserModelCase(BaseTestCase):
    """
    Unit test for the User model
    """
    def test_create_user(self):
        """
        Test that creation of user model is successful and goes as planned
        """
        user = User(name="user", email="email@email.com")
        self.assertEqual(user.name, "user")
        self.assertEqual(user.email, "email@email.com")
        self.assertNotEqual(user.name, "User")
        self.assertNotEqual(user.email, "Email@email.com")

    def test_password_hashing(self):
        """
        Test password hashing methods
        """
        u = User(name="String", email="string@email.com")
        u.set_password('StringPassword')
        self.assertTrue(u.check_password('StringPassword'))
        self.assertFalse(u.check_password('NotStringPassword'))


# unit tests for the book model
class BookModelCase(BaseTestCase):
    """
    Unit test for the book model
    """
    def test_create_book(self):
        """
        Test that creation of user model is successful and goes as planned
        """
        book = Book(
            synopsis="A very short story",
            title="Short Story",
            author="Story A. Teller",
            year_of_publish=2000
        )
        self.assertEqual(book.synopsis, "A very short story")
        self.assertEqual(book.title, "Short Story")
        self.assertEqual(book.author, "Story A. Teller")
        self.assertEqual(book.year_of_publish, 2000)


# System Tests
class RoutesTestCase(BaseTestCase):
    """
    System test for our core app routes
    """
    def test_index(self):
        with self.client() as c:
            # ensure test automatically handles redirects
            response = c.get('/', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            # homepage requires users to log in and therefore redirects users to login page
            # ensure that the response is a redirect to login page
            self.assertEqual(response.request.path, '/auth/login')

    def test_add_book(self):
        self.login()
        with self.client() as c:
            response = c.post('/admin/add-book', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        self.login()
        with self.client() as c:
            response = c.get('/admin/update/<id>', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        self.login()
        with self.client() as c:
            response = c.get('/admin/delete-book/<id>', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_auth_components(self):
        """
        Tests the register user and log in user routes
        """
        # test register user component
        with self.client() as c:
            response = c.post('/auth/register', data={
                'username': 'Testuser',
                'email': 'testuser@email.com',
                'password': 'password',
                'password2': 'password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        # test log in component
        with self.client() as c:
            response = c.post('/auth/login', data={
                'username': 'Testuser',
                'password': 'password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.login()
        with self.client() as c:
            response = c.get('/auth/logout', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.path, '/auth/login')


if __name__ == "__main__":
    unittest.main()
