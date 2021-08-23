from http import HTTPStatus


class ApplicationException(Exception):
    def __init__(self, message="Internal Server Error", status=HTTPStatus.INTERNAL_SERVER_ERROR,
                 exception: Exception = None):
        self.status = status
        self.message = message
        self.exception = exception
