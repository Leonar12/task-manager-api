from rest_framework import serializers
from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id", "owner", "title", "description",
            "priority", "status", "due_date",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "priority", "status", "due_date")

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value.strip()
