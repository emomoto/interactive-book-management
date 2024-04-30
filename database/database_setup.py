import sqlite3
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = getenv("DATABASE_PATH")

conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

def init_db():
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

def populate_sample_books():
    sample_books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565'),
        ('1984', 'George Orwell', '9780451524935'),
        ('To Kill a Mockingbird', 'Harper Lee', '9780061120084'),
        ('The Catcher in the Rye', 'J.D. Salinger', '9780316769488'),
    ]

    c.executemany('INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)', sample_books)
    conn.commit()

if __name__ == "__main__":
    init_db()
    populate_sample_books()
    print("Database initialized and sample books added.")

conn.close()