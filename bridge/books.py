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

#class DeploydBooks
