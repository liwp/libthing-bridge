class DummyTagService(object):
    def __init__(self):
        self.tags = {
            "08FD741F":
            {"tag": "08FD741F", "first": "Lauri", "last": "Pesonen", "id": "lauri.pesonen"},
            "B2C6C41C":
            {"tag": "B2C6C41C", "first": "Mark", "last": "Cheverton", "id": "mark.cheverton"},
            "825BC71C":
            {"tag": "825BC71C", "first": "Testy", "last": "Tester", "id": "testy.tester"},
        }
        
    def lookup_tag(self, tag):
        key = '%08X' % tag
        print "KEY: %s" % key
        return self.tags.get(key, None)
