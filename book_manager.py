import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")

def create_db_connection(database_file):
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        print("Connection established.")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return connection

def init_books_table(connection):
    create_table_query = """ CREATE TABLE IF NOT EXISTS books (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    author text NOT NULL,
                                    isbn text UNIQUE NOT NULL,
                                    available integer NOT NULL
                                ); """
    try:
        connection.execute(create_table_query)
        print("Table created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_book(connection, book_details):
    insert_query = ''' INSERT INTO books(title, author, isbn, available)
              VALUES(?,?,?,?) '''
    try:
        connection.execute(insert_query, book_details)
        connection.commit()
        print("Book added successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to add book. ISBN must be unique.", e)
    except Error as e:
        print(f"An unexpected error occurred: {e}")

def search_books(connection, **search_criteria):
    if not search_criteria:
        print("No search criteria provided.")
        return

    conditions = [f"{key} = '{value}'" for key, value in search_criteria.items()]
    select_query = f'SELECT * FROM books WHERE {" AND ".join(conditions)}'
    try:
        cursor = connection.cursor()
        cursor.execute(select_query)
        books = cursor.fetchall()
        if books:
            for book in books:
                print(book)
        else:
            print("No books found matching the criteria.")
    except Error as e:
        print("Failed to retrieve books.", e)

def mark_book_as_checked_out(connection, isbn):
    update_query = 'UPDATE books SET available = 0 WHERE isbn = ?'
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, (isbn,))
        connection.commit()
        if cursor.rowcount == 0:
            print("Checkout failed. Book not found.")
        else:
            print("Book checked out successfully")
    except Error as e:
        print("Checkout failed.", e)

def main():
    db_connection = create_db_connection(DATABASE_PATH)
    if db_connection is not None:
        try:
            init_books_table(db_connection)
            insert_book(db_connection, ("Python Programming", "Jon Doe", "1234", 1))
            print("Books by Jon Doe:")
            search_books(db_connection, author="Jon Doe")
            mark_book_as_checked_out(db_connection, "1234")
        except Error as e:
            print(f"An error occurred: {e}")
        finally:
            db_connection.close()
    else:
        print("Failed to create database connection.")

if __name__ == '__main__':
    main()