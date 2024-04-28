import click
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class BookManager:
    
    def __init__(self):
        self.books = []
    
    def add_book(self, title, author):
        self.books.append({"title": title, "author": author, "checked_out": False})
        return f"Book '{title}' by {author} added successfully."

    def search_books(self, title=None, author=None):
        found_books = []
        for book in self.books:
            if title and title.lower() in book["title"].lower():
                found_books.append(book)
            elif author and author.lower() in book["author"].lower():
                found_books.append(book)
        return found_books

    def checkout_book(self, title):
        for book in self.books:
            if book["title"].lower() == title.lower() and not book["checked_out"]:
                book["checked_out"] = True
                return f"Book '{title}' checked out successfully."
        return "Book not found or already checked out."

book_manager = BookManager()

@click.group()
def main():
    pass

@main.command()
@click.option('--title', required=True, help='The title of the book.')
@click.option('--author', required=True, help='The author of the book.')
def add(title, author):
    result = book_manager.add_book(title, author)
    click.echo(result)

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
    result = book_manager.checkout_book(title)
    click.echo(result)

if __name__ == "__main__":
    main()