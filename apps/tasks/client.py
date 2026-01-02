from .models import Task

class TasksClient:
    """
    Public interface for the Tasks app.
    """
    
    def get_user_task_count(self, user):
        """Returns the count of tasks assigned to a user."""
        return Task.objects.filter(assigned_to=user).count()

    def get_manager_task_count(self, user):
        """Returns the count of tasks created by a manager."""
        return Task.objects.filter(created_by=user).count()
