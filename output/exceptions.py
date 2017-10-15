class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DataError(Error):
    """Exception raised when there is a problem in the data.

    Attributes:
        data -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, data, message):
        self.data = data
        self.message = message


class OutputError(Error):
    """Exception raised when the output has a problem.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
