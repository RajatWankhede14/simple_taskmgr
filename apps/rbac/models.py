from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

User = get_user_model()


class Policy(BaseModel):
    name = models.CharField(_("policy name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.name

class Role(BaseModel):
    name = models.CharField(_("role name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.name

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="roles")

    class Meta:
        unique_together = ("role", "policy")

    def __str__(self):
        return f"{self.role.name} - {self.policy.name}"

class UserRole(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_users")

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
