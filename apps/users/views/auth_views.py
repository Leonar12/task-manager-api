from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
)


@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    """Create a new user account."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Auto-generate tokens on registration
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Account created successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Auth"])
class LoginView(TokenObtainPairView):
    """Authenticate with email + password. Returns JWT tokens and user data."""
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=["Auth"])
class TokenRefreshView(TokenRefreshView):
    """Return a new access token using a valid refresh token."""


@extend_schema(
    tags=["Auth"],
    request={"application/json": {"type": "object", "properties": {"refresh": {"type": "string"}}}},
    responses={205: None},
)
class LogoutView(generics.GenericAPIView):
    """Blacklist the refresh token to invalidate the session."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class ChangePasswordView(generics.UpdateAPIView):
    """Change the authenticated user's password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully."})
