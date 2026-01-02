from rest_framework import permissions
from apps.rbac.client import RBACClient

class TaskPermission(permissions.BasePermission):
    """
    Manager: Full CRUD.
    Reportee: View assigned tasks, Update status only to COMP.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        rbac = RBACClient()
        
        if rbac.has_role(user, "MANAGER"):
            return True # Managers can do anything
            
        if rbac.has_role(user, "REPORTEE"):
            # Reportees can only view or update tasks assigned to them
            if request.method in permissions.SAFE_METHODS:
                return obj.assigned_to == user
            
            if request.method in ["PUT", "PATCH"]:
                # The logic for "only COMP" is handled in the serializer validation
                return obj.assigned_to == user
                
        return False
