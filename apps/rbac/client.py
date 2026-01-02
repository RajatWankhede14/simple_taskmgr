from .models import Role, UserRole, Policy, RolePermission

class RBACClient:
    """
    Public interface for the RBAC app.
    Other apps should use this client instead of importing models directly.
    """
    
    def has_role(self, user, role_name):
        """Checks if a user has a specific role."""
        if not user or not user.is_authenticated:
            return False
        return UserRole.objects.filter(user=user, role__name=role_name).exists()

    def has_policy(self, user, policy_name):
        """Checks if a user has a specific policy through any of their roles."""
        if not user or not user.is_authenticated:
            return False
        return RolePermission.objects.filter(
            role__role_users__user=user,
            policy__name=policy_name
        ).exists()

    def assign_role(self, user, role_name):
        """Assigns a role to a user. Creates the role if it doesn't exist."""
        role, _ = Role.objects.get_or_create(name=role_name)
        UserRole.objects.get_or_create(user=user, role=role)

    def remove_role(self, user, role_name):
        """Removes a role from a user."""
        UserRole.objects.filter(user=user, role__name=role_name).delete()
