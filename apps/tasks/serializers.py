from rest_framework import serializers
from .models import Task, Category
from apps.authentication.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source="assigned_to", read_only=True)
    created_by_detail = UserSerializer(source="created_by", read_only=True)
    categories_detail = CategorySerializer(source="categories", many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id", "title", "description", "status", 
            "categories", "categories_detail",
            "assigned_to", "assigned_to_detail", 
            "created_by", "created_by_detail",
            "created_at", "updated_at"
        )
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_assigned_to(self, value):
        user = self.context["request"].user
        if value.company != user.company:
            raise serializers.ValidationError("You can only assign tasks to users within your company.")
        return value

    def validate_status(self, value):
        user = self.context["request"].user
        if user.is_reportee and value != Task.Status.COMP:
            raise serializers.ValidationError("Reportees can only set status to COMP.")
        return value
