import traceback, sys

class DummyBooks(object):
    def __init__(self):
        self.db = {"1":
                   {"isbn": "1",
                    "title": "Building wireless sensor networks",
                    "count": 2},
                   "2":
                   {"isbn": "2",
                    "title": "Programming Ruby",
                    "count": 1}}

        self.accounts = {}
        
    def lookup_book(self, isbn):
        if isbn in self.db:
            return self.db[isbn]
        else:
            return None

    def borrow_or_return_book(self, tag, isbn):
        try:
            if tag in self.accounts and isbn in self.accounts[tag]:
                self.return_book(tag, isbn)
                return 'R'
            else:
                self.borrow_book(tag, isbn)
                return 'B'
        except:
            print "Unexpected error:", sys.exc_info()[0]
            traceback.print_exc(file=sys.stdout)
            return 'F'

    def borrow_book(self, tag, isbn):
        # TODO: return errors for asserts
        assert isbn in self.db
        assert self.db[isbn]['count'] > 0
        assert isbn not in self.accounts.get(tag, [])
        
        self.db[isbn]['count'] -= 1
        account = self.accounts.get(tag, [])
        account.append(isbn)
        self.accounts[tag] = account
        
    def return_book(self, tag, isbn):
        # TODO: return errors for asserts
        assert tag in self.accounts
        assert isbn in self.db
        assert isbn in self.accounts[tag]

        self.db[isbn]['count'] += 1
        self.accounts[tag].remove(isbn)

import json
import requests
class DeploydBooks(object):
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/ ') # remove trailing slash (and spaces)

    def lookup_book(self, isbn):
        print self.isbn_url(isbn)
        r = requests.get(self.isbn_url(isbn))
        books = r.json()
        print books
        if len(books) == 0:
            return None
        else:
            book = books[0]
            if 'borrower' in book:
                del book['borrower']
            return book

    def borrow_or_return_book(self, tag, isbn):
        r = requests.get(self.isbn_url(isbn))
        books = r.json()
        if r.status_code != 200:
            print "Books request failed: %s - %s" % (r.status_code, books)
            return 'F'

        if not books:
            print "Book with ISBN %s does not exist in the library" % isbn
            return 'F'

        borrowed_book = next((b for b in books if b.get('borrower') == str(tag)), None)
        if borrowed_book:
            return self.return_book(borrowed_book['id'])
        else:
            free_books = [ b['id'] for b in books if b.get('borrower','') == '' ]
            if len(free_books) == 0:
                print "All books have been lent!: %s" % books
                return 'F'
            else:
                return self.borrow_book(tag, free_books[0])
        
    def borrow_book(self, tag, book_id):
        print "BORROW"
        print tag
        url = self.book_url(book_id)
        data = json.dumps({u'borrower': str(tag)})
        print url
        print data
        r = requests.put(url, data=data)
        book = r.json()
        if r.status_code == 200:
            print "Book borrowed!"
            print book
            return 'B'
        else:
            print "Borrowing book failed: %s - %s" % (r.status_code, book)
            return 'F'
        
    def return_book(self, book_id):
        print "RETURN"
        r = requests.put(self.book_url(book_id), data=json.dumps({u'borrower': ''}))
        print r.json()
        if r.status_code == 200:
            print "Book returned!"
            return 'R'
        else:
            print "Returning book failed: %s - %s" % (r.status_code, r.json())
            return 'F'

    def isbn_url(self, isbn):
        return '%s/?isbn=%s' % (self.base_url, isbn)

    def book_url(self, book_id):
        return '%s/%s' % (self.base_url, book_id)
