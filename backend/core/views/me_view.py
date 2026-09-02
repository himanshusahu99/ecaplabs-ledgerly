"""Endpoint describing the signed-in user."""

from core.abstractions.base_view import BaseView
from core.repositories.business_repository import BusinessRepository
from rest_framework.response import Response


class MeView(BaseView):
    """Returns the signed-in user and the businesses they can access."""

    def get(self, request):
        businesses = BusinessRepository().list_for_user(user=request.user)
        return Response(
            {
                "email": request.user.email,
                "businesses": [
                    {"business_id": business.business_id, "name": business.name}
                    for business in businesses
                ],
            }
        )
