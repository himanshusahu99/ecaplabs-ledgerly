"""Base class for business logic."""


class BaseService:
    """Coordinates repositories and clients; holds no ORM queries itself."""

    def __init__(self, **kwargs):
        self.options = kwargs
