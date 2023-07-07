class PermissionDeniedException(Exception):
    pass


class NotFoundException(Exception):
    pass

class BadRequestException(Exception):
    pass

class CustomException(Exception):
    def __init__(self, status_code, message, error_code) -> None:
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
