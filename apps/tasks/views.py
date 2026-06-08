from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskCreateUpdateSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Tasks"],
        summary="List all tasks",
        description="Returns a paginated list of all tasks owned by the authenticated user.",
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, description="Filter by status (pending, in_progress, done)"),
            OpenApiParameter("priority", OpenApiTypes.STR, description="Filter by priority (low, medium, high)"),
            OpenApiParameter("search", OpenApiTypes.STR, description="Search by title or description"),
        ],
    ),
    create=extend_schema(tags=["Tasks"], summary="Create a task"),
    retrieve=extend_schema(tags=["Tasks"], summary="Get a task by ID"),
    update=extend_schema(tags=["Tasks"], summary="Update a task (full)"),
    partial_update=extend_schema(tags=["Tasks"], summary="Partially update a task"),
    destroy=extend_schema(tags=["Tasks"], summary="Delete a task"),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for authenticated user's tasks.

    Each user can only access and manage their own tasks.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority"]

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        tags=["Tasks"],
        summary="Get task summary stats",
        description="Returns counts grouped by status for the authenticated user.",
    )
    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "pending": qs.filter(status=Task.Status.PENDING).count(),
            "in_progress": qs.filter(status=Task.Status.IN_PROGRESS).count(),
            "done": qs.filter(status=Task.Status.DONE).count(),
        })
