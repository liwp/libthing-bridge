class DummyTags(object):
    def __init__(self):
        self.tags = {
            "08FD741F":
            {"tag": "08FD741F", "firstname": "Lauri", "lastname": "Pesonen", "username": "lauri.pesonen"},
            "B2C6C41C":
            {"tag": "B2C6C41C", "firstname": "Mark", "lastname": "Cheverton", "username": "mark.cheverton"},
            "825BC71C":
            {"tag": "825BC71C", "firstname": "Testy", "lastname": "Tester", "username": "testy.tester"},
        }
        
    def lookup_tag(self, tag):
        key = '%08X' % tag
        print "KEY: %s" % key
        return self.tags.get(key)

# third party lib: http://docs.python-requests.org/en/latest/
import requests
class DeploydTags(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def lookup_tag(self, tag):
        r = requests.get(self.tag_url(tag))
        response = r.json()

        if len(response) == 0:
            return None
        elif len(response) == 1:
            return response[0]
        else:
            assert False, "Expected one tag in response, got %d: %s" % (len(response), response)

    def tag_url(self, tag):
        return '%s/?{"tag":%d}' % (self.base_url, tag)
