"""Exception types shared across apps and the API error handler."""

import logging

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class BaseAPIException(APIException):
    """An error that maps cleanly to an HTTP response."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."


class ObjectNotFoundError(BaseAPIException):
    """The requested record does not exist or is not visible to the caller."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found."


class ConflictError(BaseAPIException):
    """The record is not in a state that allows the requested action."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict."


class ExternalServiceError(Exception):
    """A call to a third-party service failed."""

    def __init__(self, *, service, message, status_code=None):
        super().__init__(f"{service}: {message}")
        self.service = service
        self.status_code = status_code


def api_exception_handler(exc, context):
    """Logs unexpected errors before DRF renders the response."""
    response = exception_handler(exc, context)
    if response is None:
        logger.exception("unhandled error in %s", context.get("view"))
    return response
