import sqlite3
from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = getenv("DATABASE_PATH")

if not DB_PATH or not path.exists(DB_PATH):
    raise EnvironmentError("DATABASE_PATH environment variable is not set correctly or database file does not exist.")

def connect_to_database():
    try:
        connection = sqlite3.connect(DB_PATH)
        return connection
    except sqlite3.Error as error:
        print(f"An error occurred while connecting to the database: {error}")
        raise error

def initialize_database():
    with connect_to_database() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS books
                        (book_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        isbn TEXT NOT NULL UNIQUE,
                        checkout_status BOOLEAN NOT NULL DEFAULT 0)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                        (transaction_id INTEGER PRIMARY KEY,
                        book_id INTEGER NOT NULL,
                        checkout_date DATE,
                        return_date DATE,
                        FOREIGN KEY (book_id) REFERENCES books(book_id))''')

            conn.commit()
        except sqlite3.Error as error:
            print(f"An error occurred while initializing the database: {error}")

def add_sample_books():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        books_to_add = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565'),
            ('1984', 'George Orwell', '9780451524935'),
            ('To Kill a Mockingbird', 'Harper Lee', '9780061120084'),
            ('The Catcher in the Rye', 'J.D. Salinger', '9780316769488'),
        ]

        try:
            cursor.executemany('INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)', books_to_add)
            conn.commit()
        except sqlite3.IntegrityError as error:
            print(f"An integrity error occurred while adding sample books: {error}")
        except sqlite3.Error as error:
            print(f"An error occurred while adding sample books: {error}")

if __name__ == "__main__":
    try:
        initialize_database()
        add_sample_books()
        print("Database initialized and sample books added successfully.")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")