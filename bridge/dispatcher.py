import unicodedata
class Dispatcher(object):
    def __init__(self, id_service, lib_service):
        self.id_service = id_service
        self.lib_service = lib_service

    def dispatch_tag_req(self, request):
        tag = request['tag']
        print "TAG REQ - %s" % tag
        id =  self.id_service.lookup_tag(tag)
        if not id:
            print "TAG RSP - no such tag: %s" % tag
            return { 'type': 'tag_rsp', 'id': None }

        firstname = unicodedata.normalize('NFKD', id['firstname']).encode('ascii','ignore')
        print "TAG RSP - name: %s" % firstname
        return { 'type': 'tag_rsp', 'id': firstname }

    def dispatch_book_req(self, request):
        isbn = request['isbn']
        print "BOOK REQ - %s" % isbn
        book = self.lib_service.lookup_book(isbn)
        if not book:
            print "BOOK RSP - no such book: %s" % isbn
            return { 'type': 'book_rsp', 'title': None }

        title = unicodedata.normalize('NFKD', book['title']).encode('ascii','ignore')
        print "BOOK RSP - book title: %s" % title
        return { 'type': 'book_rsp', 'title': title }
    
    def dispatch_lending_req(self, request):
        tag = request['tag']
        isbn = request['isbn']
        print "LENDING REQ - %s %s" % (tag, isbn)
        result = self.lib_service.borrow_or_return_book(tag, isbn)
        print "LENDING RSP - %s" % result
        return { 'type': 'lending_rsp', 'result': result }
    
    def dispatch(self, request):
        return {
            'tag_req': self.dispatch_tag_req,
            'book_req': self.dispatch_book_req,
            'lending_req': self.dispatch_lending_req,
        }[request['type']](request)
