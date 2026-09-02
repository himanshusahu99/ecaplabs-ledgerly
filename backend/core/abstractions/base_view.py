"""Base class for API views."""

from core.permissions import IsBusinessMember
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseView(APIView):
    """An authenticated view; subclasses stay thin and call one service."""

    permission_classes = [IsAuthenticated]


class BaseBusinessView(BaseView):
    """A view scoped to the business in the URL."""

    permission_classes = [IsAuthenticated, IsBusinessMember]
