""" A StringBuilder class for string buffer addicts.
"""
import io

class StringBuilder:

    def __init__(self):
        self.empty = True
        self._stringio = io.StringIO()

    def __str__(self):
        val = self._stringio.getvalue()
        self._stringio.close()
        return val

    # this one returns the string buffer (and so could be closed by a print)
    def append(self, obj):
        data = str(obj)
        if self.empty and len(data) > 0:
            self.empty = False
        self._stringio.write(data)
        return self

    # this one returns None
    def add(self, obj):
        data = str(obj)
        if self.empty and len(data) > 0:
            self.empty = False
        self._stringio.write(data)

    def isempty(self):
        return self.empty
