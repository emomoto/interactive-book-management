import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_PATH")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        author text NOT NULL,
                                        isbn text UNIQUE NOT NULL,
                                        available integer NOT NULL
                                    ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_books_table)
    except Error as e:
        print(e)

def add_book(conn, book):
    sql = ''' INSERT INTO books(title, author, isbn, available)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, book)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Failed to add book. ISBN must be unique.", e)

def retrieve_books(conn, **kwargs):
    sql = 'SELECT * FROM books WHERE'
    conditions = []
    for key, value in kwargs.items():
        if key in ['title', 'author', 'isbn', 'available']:
            conditions.append(f"{key} = '{value}'")
    sql += ' AND '.join(conditions)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def checkout_book(conn, isbn):
    sql = 'UPDATE books SET available = 0 WHERE isbn = ?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (isbn,))
        conn.commit()
        if cur.rowcount == 0:
            print("Checkout failed. Book not found.")
        else:
            print("Book checked out successfully")
    except Error as e:
        print("Checkout failed", e)

if __name__ == '__main__':
    conn = create_connection(DATABASE)
    if conn is not None:
        create_table(conn)
        add_book(conn, ("Python Programming", "Jon Doe", "1234", 1))
        print("Books by Jon Doe:")
        retrieve_books(conn, author="Jon Doe")
        checkout_book(conn, "1234")
        if conn:
            conn.close()