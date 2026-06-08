from django.urls import path
from apps.users.views.user_views import ProfileView

urlpatterns = [
    path("me/", ProfileView.as_view(), name="user-profile"),
]
