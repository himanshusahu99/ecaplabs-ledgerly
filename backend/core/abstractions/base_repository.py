"""Base class for data access objects."""

import functools
import logging
import time

logger = logging.getLogger(__name__)


class BaseRepository:
    """Owns every ORM query for one model."""

    model = None

    @property
    def objects(self):
        """Returns the model manager."""
        if self.model is None:
            raise AttributeError(f"{type(self).__name__} has no model")
        return self.model.objects

    @staticmethod
    def log_execution_time(detail):
        """Logs how long a repository method took."""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                started = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    logger.debug(
                        "%s took %.3fs | %s",
                        func.__qualname__,
                        time.perf_counter() - started,
                        detail,
                    )

            return wrapper

        return decorator
