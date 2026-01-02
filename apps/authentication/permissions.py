from rest_framework import permissions
from apps.rbac.client import RBACClient

class IsManager(permissions.BasePermission):
    """
    Allows access only to users with the MANAGER role via RBAC.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and RBACClient().has_role(request.user, "MANAGER"))

class IsReportee(permissions.BasePermission):
    """
    Allows access only to users with the REPORTEE role via RBAC.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and RBACClient().has_role(request.user, "REPORTEE"))
