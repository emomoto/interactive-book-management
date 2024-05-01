import sqlite3
from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = getenv("DATABASE_PATH")

if not DATABASE_PATH or not path.exists(DATABASE_PATH):
    raise EnvironmentError("DATABASE_PATH environment variable is not set correctly or database file does not exist.")

try:
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
except sqlite3.Error as e:
    print(f"An error occurred while connecting to the database: {e}")
    raise e

def init_db():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS books
                    (book_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL UNIQUE,
                    checkout_status BOOLEAN NOT NULL DEFAULT 0)''')

        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (transaction_id INTEGER PRIMARY KEY,
                    book_id INTEGER NOT NULL,
                    checkout_date DATE,
                    return_date DATE,
                    FOREIGN KEY (book_id) REFERENCES books(book_id))''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

def populate_sample_books():
    sample_books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565'),
        ('1984', 'George Orwell', '9780451524935'),
        ('To Kill a Mockingbird', 'Harper Lee', '9780061120084'),
        ('The Catcher in the Rye', 'J.D. Salinger', '9780316769488'),
    ]

    try:
        c.executemany('INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)', sample_books)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"An integrity error occurred while populating sample books: {e}")
    except sqlite3.Error as e:
        print(f"An error occurred while populating sample books: {e}")

if __name__ == "__main__":
    try:
        init_db()
        populate_sample_books()
        print("Database initialized and sample books added.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        conn.close()