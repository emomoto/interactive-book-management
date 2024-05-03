class BookManager:
    def __init__(self, database_url):
        pass
    
    def reset_database(self):
        pass

    def add_books_bulk(self, books):
        pass

    def get_books_bulk(self, titles):
        pass

class TestBookManager(unittest.TestCase):
    def test_add_books_bulk(self):
        books_to_add = [('Python 101', 'Eric', 2021), ('Advanced Python', 'Jane', 2022)]
        self.assertTrue(self.book_manager.add_books_bulk(books_to_add))
        self.assertIsNotNone(self.book_manager.get_book('Python 101'))
        self.assertIsNotNone(self.book_manager.get_book('Advanced Python'))