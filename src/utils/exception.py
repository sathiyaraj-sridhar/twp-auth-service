"""
Utility for manage custom exceptions.
"""


class ValidationError(Exception):
    """Raised when validation fails"""
    def __init__(self, message="Invalid input"):
        self.message = message
        super().__init__(self.message)
