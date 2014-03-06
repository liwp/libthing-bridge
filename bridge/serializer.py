import struct

class Serializer(object):
    def __init__(self):
        self.codes = {
            'T': self.deserialize_tag_request,
            'B': self.deserialize_book_request,
            'L': self.deserialize_lending_request
        }

    def deserialize_request(self, req):
        code = req[0]
        payload = req[1:]
        print "REQUEST code: %s" % code
        print "PAYLOAD: %s" % self.hex_dump(code)
        print "PAYLOAD: %s" % self.hex_dump(payload)
        
        if code in self.codes:
            return self.codes[code](payload)

    def deserialize_tag_request(self, req):
        payload = struct.unpack('>L', req)
        return { 'type': 'tag_req',
                 'tag': payload[0] }

    def deserialize_book_request(self, req):
        payload =  struct.unpack('<128p', req)
        return { 'type': 'book_req',
                 'isbn': payload[0] }

    def deserialize_lending_request(self, req):
        payload =  struct.unpack('<L128p', req)
        return { 'type': 'lending_req',
                 'tag': payload[0], 'isbn': payload[1] }
    
    def serialize_response(self, rsp):
        return {
            'tag_rsp': self.serialize_tag_response,
            'book_rsp': self.serialize_book_response,
            'lending_rsp': self.serialize_lending_response
        }[rsp['type']](rsp)

    def serialize_tag_response(self, rsp):
        return struct.pack('<c128p', 'T', rsp['id'] or '')

    def serialize_book_response(self, rsp):
        return struct.pack('<c128p', 'B', rsp['title'] or '')

    def serialize_lending_response(self, rsp):
        return struct.pack('<cc', 'L', rsp['result'])

    def hex_dump(self, req):
        return ':'.join(x.encode('hex') for x in req)
    
