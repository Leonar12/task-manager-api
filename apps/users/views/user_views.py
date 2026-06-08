from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from apps.users.models import User
from apps.users.serializers import UserSerializer


@extend_schema(tags=["Users"])
class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
