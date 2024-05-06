#!/usr/bin/env python3

from library_xmlrpc import LibraryAPI
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('command', choices=['list', 'add', 'set', 'del'])
parser.add_argument('params', nargs='*')
args = parser.parse_args()

# Sample test configurations
host, port, db = 'localhost', '8069', 'library'
user, pwd = 'admin', 'admin'
api = LibraryAPI(host, port, db, user, pwd)

if args.command == 'list':
    title = args.params[0]

    books = api.search_read(title)
    for book in books:
        print(f"{book['id']} - {book['name']}")

elif args.command == 'add':
    title = args.params[0]
    book_id = api.create(title)
    print(f"Book added with ID {book_id} with title {title}")

elif args.command == 'set':
    if len(args.params) != 2:
        print("set command requires a Title and ID.")
    else:
        book_id, title = int(args.params[0]), args.params[1]
        api.write(book_id, title)
        print(f"Book {book_id} updated with title {title}")

elif args.command == 'del':
    book_id = int(args.params[0])
    api.unlink(book_id)
    print(f"Book {book_id} deleted.")

