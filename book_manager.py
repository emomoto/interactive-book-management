import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_PATH")

def create_connection(db_file):
    try:
        with sqlite3.connect(db_file) as conn:
            return conn
    except Error as e:
        print(e)
    return None

def create_table(conn):
    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    author text NOT NULL,
                                    isbn text UNIQUE NOT NULL,
                                    available integer NOT NULL
                                ); """
    try:
        with conn:
            conn.execute(sql_create_books_table)
    except Error as e:
        print(e)

def add_book(conn, book):
    sql = ''' INSERT INTO books(title, author, isbn, available)
              VALUES(?,?,?,?) '''
    try:
        with conn:
            conn.execute(sql, book)
    except sqlite3.IntegrityError as e:
        print("Failed to add book. ISBN must be unique.", e)

def retrieve_books(conn, **kwargs):
    sql = 'SELECT * FROM books WHERE'
    conditions = [f"{key} = '{value}'" for key, value in kwargs.items() if key in ['title', 'author', 'isbn', 'available']]
    sql += ' AND '.join(conditions)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except Error as e:
        print("Failed to retrieve books.", e)

def checkout_book(conn, isbn):
    sql = 'UPDATE books SET available = 0 WHERE isbn = ?'
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(sql, (isbn,))
            if cur.rowcount == 0:
                print("Checkout failed. Book not found.")
            else:
                print("Book checked out successfully")
    except Error as e:
        print("Checkout failed.", e)

if __name__ == '__main__':
    with create_connection(DATABASE) as conn:
        if conn is not None:
            create_table(conn)
            add_book(conn, ("Python Programming", "Jon Doe", "1234", 1))
            print("Books by Jon Doe:")
            retrieve_books(conn, author="Jon Doe")
            checkout_book(conn, "1234")