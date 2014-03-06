class Dispatcher(object):
    def __init__(self, id_service, lib_service):
        self.id_service = id_service
        self.lib_service = lib_service

    def dispatch_tag_req(self, request):
        print "TAG REQ: %s" % request
        id =  self.id_service.lookup_tag(request['tag'])
        print "TAG RSP: %s" % id
        return { 'type': 'tag_rsp',
                 'id': id['firstname'] if id else None }

    def dispatch_book_req(self, request):
        print "BOOK REQ: %s" % request
        book = self.lib_service.lookup_book(request['isbn'])
        return { 'type': 'book_rsp',
                 'title': book['title'] if book else None }
    
    def dispatch_lending_req(self, request):
        print "LENDING REQ: %s" % request
        result = self.lib_service.borrow_or_return_book(request['tag'], request['isbn'])
        return { 'type': 'lending_rsp',
                 'result': result }
    
    def dispatch(self, request):
        return {
            'tag_req': self.dispatch_tag_req,
            'book_req': self.dispatch_book_req,
            'lending_req': self.dispatch_lending_req,
        }[request['type']](request)
