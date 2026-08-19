class AppException(Exception):
    def __init__(
        self,
        error: str,
        message: str,
        status_code: int
    ):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class BookNotFoundException(AppException):
    def __init__(self, message="Book not found"):
        super().__init__(
            error="BOOK_NOT_FOUND",
            message=message,
            status_code=404
        )