class DomainException(Exception):
    """Base class for domain exceptions."""
    def __init__(
        self,
        message: str,
        type: str = "DomainException",
        field: str | None = None,
        error_code: int | None = None,
    ):
        self.field = field
        self.message = message
        self.type = type
        self.error_code = error_code

        super().__init__(f"{field}: {message}")
class ApplicationException(Exception):
    """Base class for domain exceptions."""
    def __init__(
        self,
        message: str,
        type: str = "ApplicationException",
        field: str | None = None,
        error_code: int | None = None,
    ):
        self.field = field
        self.message = message
        self.type = type
        self.error_code = error_code

        super().__init__(f"{field}: {message}")
