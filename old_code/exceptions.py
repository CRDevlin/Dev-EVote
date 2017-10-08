class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidFileError(Error):
    def __init__(self, message='Invalid file specified'):
        self.message = message
