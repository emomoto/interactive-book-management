import click
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class BookManager:
    
    def __init__(self):
        self.books = []
    
    def add_book(self, title, author):
        book = {"title": title, "author": author, "checked_out": False}
        self.books.append(book)
        logging.info(f"Book '{title}' by {author} added to the collection.")
        return f"Book '{title}' by {author} added successfully."

    def search_books(self, title=None, author=None):
        def matches(book):
            if title:
                return title.lower() in book["title"].lower()
            if author:
                return author.lower() in book["author"].lower()
            return False
        found_books = [book for book in self.books if matches(book)]
        
        log_message = "Search successful. Books found." if found_books else "No books matched the search criteria."
        logging.info(log_message)
        
        return found_books

    def checkout_book(self, title):
        for book in self.books:
            if book["title"].lower() == title.lower() and not book["checked_out"]:
                book["checked_out"] = True
                logging.info(f"Book '{title}' checked out successfully.")
                return f"Book '{title}' checked out successfully."
        logging.warning(f"Book '{title}' not found or already checked out.")
        return f"Book '{title}' not found or already checked out."

book_manager = BookManager()

@click.group()
def main():
    pass

@main.command()
@click.option('--title', required=True, help='The title of the book.')
@click.option('--author', required=True, help='The author of the book.')
def add(title, author):
    click.echo(book_manager.add_book(title, author))

@main.command()
@click.option('--title', help='Search for books by title.')
@click.option('--author', help='Search for books by author.')
def search(title, author):
    if not title and not author:
        click.echo("Please specify a title or an author to search for.")
        return

    found_books = book_manager.search_books(title, author)
    if found_books:
        for book in found_books:
            click.echo(f"Title: {book['title']}, Author: {book['author']}, Checked Out: {book['checked_out']}")
    else:
        click.echo("No books found.")

@main.command()
@click.option('--title', required=True, help='The title of the book to check out.')
def checkout(title):
    click.echo(book_manager.checkout_book(title))

if __name__ == "__main__":
    main()