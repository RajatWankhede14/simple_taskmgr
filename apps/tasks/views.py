from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission
from apps.core.throttling import TaskCreateThrottle, TaskListThrottle

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    def get_throttles(self):
        if self.action == "create":
            return [TaskCreateThrottle()]
        if self.action == "list":
            return [TaskListThrottle()]
        return super().get_throttles()

    def get_queryset(self):
        user = self.request.user
        if not user.company:
            return Task.objects.none()
            
        if user.is_manager:
            return Task.objects.filter(created_by__company=user.company)
        if user.is_reportee:
            return Task.objects.filter(assigned_to=user)
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
