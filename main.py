import click
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class LibraryManagementSystem:
    
    def __init__(self):
        self.catalog = []  # Changed from 'books' for more specificity
    
    def add_book_to_catalog(self, title, author):
        new_book = {"title": title, "author": author, "is_checked_out": False}  # Renamed variables for clarity
        self.catalog.append(new_book)
        logging.info(f"Book '{title}' by {author} added to the library catalog.")
        return f"Book '{title}' by {author} added successfully."

    def find_books(self, title=None, author=None):
        def is_match(book):
            if title and title.lower() in book["title"].lower():
                return True
            if author and author.lower() in book["author"].lower():
                return True
            return False
        matched_books = [book for book in self.catalog if is_match(book)]
        
        log_message = "Search successful. Books found." if matched_books else "No books matched the search criteria."
        logging.info(log_message)
        
        return matched_books

    def loan_out_book(self, title):
        for book in self.catalog:
            if book["title"].lower() == title.lower() and not book["is_checked_out"]:
                book["is_checked_out"] = True
                logging.info(f"Book '{title}' has been loaned out successfully.")
                return f"Book '{title}' has been loaned out successfully."
        logging.warning(f"Book '{title}' not found or already loaned out.")
        return f"Book '{title}' not found or already loaned out."

library_system = LibraryManagementSystem()

@click.group()
def main():
    pass

@main.command()
@click.option('--title', required=True, help='The title of the book.')
@click.option('--author', required=True, help='The author of the book.')
def add(title, author):
    click.echo(library_system.add_book_to_catalog(title, author))

@main.command()
@click.option('--title', help='Search books by title.')
@click.option('--author', help='Search books by author.')
def search(title, author):
    if not title and not author:
        click.echo("Please specify a title or an author for the search.")
        return

    matched_books = library_system.find_books(title, author)
    if matched_books:
        for book in matched_books:
            click.echo(f"Title: {book['title']}, Author: {book['author']}, Loaned Out: {book['is_checked_out']}")
    else:
        click.echo("No matching books found.")

@main.command()
@click.option('--title', required=True, help='The title of the book to loan out.')
def checkout(title):
    click.echo(library_system.loan_out_book(title))

if __name__ == "__main__":
    main()