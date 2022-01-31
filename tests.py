"""
A module containing the application's test suite
"""
import unittest
from app.models import Book, User
from app import db
from main import app


# Unit Tests
class UserModelCase(unittest.TestCase):
    """
    Unit test for the User model
    """
    def setUp(self):
        """
        Set up database temporarily
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        """
        Destroy temporary database
        """
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        """
        Test password hashing methods
        """
        u = User(username="String")
        u.set_password('StringPassword')
        self.assertTrue(u.check_password('StringPassword'))
        self.assertFalse(u.check_password('NotStringPassword'))


# System Tests
class AppTestCase(unittest.TestCase):
    """
    System test for our core app routes
    """
    def test_index(self):
        with app.test_client() as c:
            response = c.get('/')

            self.assertEqual(response.status_code, 302)

    def test_book_search(self):
        with app.test_client() as c:
            response = c.get('/books/s/<name>')

            self.assertEqual(response.status_code, 200)

    def test_add_book(self):
        with app.test_client() as c:
            response = c.get('/add-book/<id>')

            self.assertEqual(response.status_code, 302)

    def test_update_book(self):
        with app.test_client() as c:
            response = c.get('/update/<id>')

            self.assertEqual(response.status_code, 302)

    def test_delete_book(self):
        with app.test_client() as c:
            response = c.get('/delete-book/<id>')

            self.assertEqual(response.status_code, 302)

    def test_login(self):
        with app.test_client() as c:
            response = c.get('/login')

            self.assertEqual(response.status_code, 302)

    def test_register(self):
        with app.test_client() as c:
            response = c.get('/logout')

            self.assertEqual(response.status_code, 302)

    def test_logout(self):
        with app.test_client() as c:
            response = c.get('/register')

            self.assertEqual(response.status_code, 302)


# API tests


if __name__ == "__main__":
    unittest.main()
    