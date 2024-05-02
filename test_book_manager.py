import unittest
from book_manager import BookManager
from unittest.mock import patch
import os

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.database_url = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
        self.book_manager = BookManager(database_url=self.database_url)
        self.book_manager.reset_database()

    def test_add_book(self):
        self.assertTrue(self.book_manager.add_book('Python 101', 'Eric', 2021))
        self.assertFalse(self.book_manager.add_book('Python 101', 'Eric', 2021))

    def test_get_book(self):
        self.book_manager.add_book('Python Testing', 'Diana', 2022)
        book = self.book_manager.get_book('Python Testing')
        self.assertIsNotNone(book)
        self.assertEqual(book['title'], 'Python Testing')
        self.assertIsNone(self.book_manager.get_book('Non Existing'))
    
    @patch('book_manager.BookManager._is_available_for_checkout')
    def test_checkout_book(self, mock_is_available):
        self.book_manager.add_book('Clean Code', 'Robert', 2008)
        mock_is_available.return_value = True
        self.assertTrue(self.book_manager.checkout_book('Clean Code', 'User1'))

        mock_is_available.return_value = False
        self.assertFalse(self.book_manager.checkout_book('Clean Code', 'User2'))

    def test_return_book(self):
        self.book_manager.add_book('Refactoring', 'Martin', 1999)
        self.book_manager.checkout_book('Refactoring', 'User1')
        self.assertTrue(self.book_manager.return_book('Refactoring', 'User1'))
        self.assertFalse(self.book_manager.return_book('Refactoring', 'User2'))

    def test_reset_database(self):
        self.book_manager.add_book('Test-Driven Development', 'Kent', 2003)
        self.book_manager.reset_database()
        self.assertIsNone(self.book_manager.get_book('Test-Driven Development'))

if __name__ == '__main__':
    unittest.main()