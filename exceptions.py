class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class DataError(Error):
    """Exception raised when the provided data is not as expected.

    Attributes:
        data -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, data, message):
        self.data = data
        self.message = message
