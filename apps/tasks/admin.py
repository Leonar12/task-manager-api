from django.contrib import admin
from apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "priority", "status", "due_date", "created_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "owner__email")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
