import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_PATH")

def create_connection(db_file):
    """Create and return a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established.")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    """Create books table if it doesn't exist."""
    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    author text NOT NULL,
                                    isbn text UNIQUE NOT NULL,
                                    available integer NOT NULL
                                ); """
    try:
        conn.execute(sql_create_books_table)
        print("Table created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

def add_book(conn, book):
    """Add a new book to the database."""
    sql = ''' INSERT INTO books(title, author, isbn, available)
              VALUES(?,?,?,?) '''
    try:
        conn.execute(sql, book)
        conn.commit()
        print("Book added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add book. ISBN must be unique.", e)
    except Error as e:
        print(f"An unexpected error occurred: {e}")

def retrieve_books(conn, **kwargs):
    """Retrieve books based on criteria."""
    if not kwargs:
        print("No search criteria provided.")
        return

    conditions = [f"{key} = '{value}'" for key, value in kwargs.items()]
    sql = f'SELECT * FROM books WHERE {" AND ".join(conditions)}'
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No books found matching the criteria.")
    except Error as e:
        print("Failed to retrieve books.", e)

def checkout_book(conn, isbn):
    """Mark a book as checked out."""
    sql = 'UPDATE books SET available = 0 WHERE isbn = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (isbn,))
        conn.commit()
        if cur.rowcount == 0:
            print("Checkout failed. Book not found.")
        else:
            print("Book checked out successfully")
    except Error as e:
        print("Checkout failed.", e)

def main():
    conn = create_connection(DATABASE)
    if conn is not None:
        try:
            create_table(conn)
            add_book(conn, ("Python Programming", "Jon Doe", "1234", 1))
            print("Books by Jon Doe:")
            retrieve_books(conn, author="Jon Doe")
            checkout_book(conn, "1234")
        except Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        print("Failed to create database connection.")

if __name__ == '__main__':
    main()