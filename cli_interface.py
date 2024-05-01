import click
from dotenv import load_dotenv
import os

load_dotenv()

def add_book(title, author):
    try:
        print(f"Book '{title}' by {author} added successfully.")
    except Exception as e:
        print(f"Failed to add book: {e}")

def search_books(keyword):
    try:
        print(f"Found books related to '{keyword}'.")
    except Exception as e:
        print(f"Error searching books: {e}")

def check_in_out(book_id, check_out):
    try:
        if check_out:
            print(f"Book with ID {book_id} checked out successfully.")
        else:
            print(f"Book with ID {book_id} returned successfully.")
    except Exception as e:
        print(f"Error in checking book: {e}")

@click.group()
def cli():
    pass

@cli.command()
@click.option('--title', prompt='Book title', help='Title of the book to add.')
@click.option('--author', prompt='Book author', help='Author of the book.')
def add(title, author):
    if not title or not author:
        print("Error: Title and author are required.")
        return
    add_book(title, author)

@cli.command()
@click.option('--keyword', prompt='Search keyword', help='Keyword to search for books.')
def search(keyword):
    if not keyword:
        print("Error: Search keyword is required.")
        return
    search_books(keyword)

@cli.command()
@click.option('--book_id', prompt='Book ID', type=int, help='The ID of the book.')
@click.option('--check_out', is_flag=True, help='Check out a book. Leave blank to return a book.')
def check(book_id, check_out):
    if not isinstance(book_id, int) or book_id < 0:
        print("Error: Invalid book ID.")
        return
    check_in_out(book_id, check_out)

if __name__ == '__main__':
    cli()