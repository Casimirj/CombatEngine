class InvalidAmmunitionException(Exception):
    """Raised when the equipped ammunition is incompatible with the weapon."""

    def __init__(self, message: str):
        super().__init__(message)
