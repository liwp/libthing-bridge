from __future__ import print_function

class Mock(object):
    def __getattr__(self, name):
        return lambda *args: print("%s%s" % (name, args))
