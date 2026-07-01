class InvalidLoadoutException(Exception):
    """Raised when a loadout configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(message)
