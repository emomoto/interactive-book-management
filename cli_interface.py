import click
from dotenv import load_dotenv
import os

load_dotenv()

def add_book(title, author):
    print(f"Book '{title}' by {author} added successfully.")

def search_books(keyword):
    print(f"Found books related to '{keyword}'.")

def check_in_out(book_id, check_out):
    if check_out:
        print(f"Book with ID {book_id} checked out successfully.")
    else:
        print(f"Book with ID {book_id} returned successfully.")

@click.group()
def cli():
    pass

@cli.command()
@click.option('--title', prompt='Book title', help='Title of the book to add.')
@click.option('--author', prompt='Book author', help='Author of the book.')
def add(title, author):
    add_book(title, author)

@cli.command()
@click.option('--keyword', prompt='Search keyword', help='Keyword to search for books.')
def search(keyword):
    search_books(keyword)

@cli.command()
@click.option('--book_id', prompt='Book ID', type=int, help='The ID of the book.')
@click.option('--check_out', is_flag=True, help='Check out a book. Leave blank to return a book.')
def check(book_id, check_out):
    check_in_out(book_id, check_out)

if __name__ == '__main__':
    cli()