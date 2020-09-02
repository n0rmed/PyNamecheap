
__all__ = ['NamecheapError', 'ApiError']


class NamecheapError(Exception):
    pass


# https://www.namecheap.com/support/api/error-codes.aspx
class ApiError(NamecheapError):
    def __init__(self, number, text):
        Exception.__init__(self, '%s - %s' % (number, text))
        self.number = number
        self.text = text

