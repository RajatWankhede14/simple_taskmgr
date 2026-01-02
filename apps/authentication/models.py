from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel, SoftDeleteManager

from django.contrib.auth.models import UserManager

class UserSoftDeleteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(AbstractUser, BaseModel):
    """
    Custom user model for the project with email/mobile as username.
    """
    objects = UserSoftDeleteManager()
    
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. Can be email or mobile."),
    )
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    mobile = models.CharField(_("mobile number"), max_length=15, unique=True, null=True, blank=True)
    company = models.ForeignKey(
        'core.Company', 
        on_delete=models.CASCADE, 
        related_name="users",
        null=True,
        blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_manager(self):
        from apps.rbac.client import RBACClient
        return RBACClient().has_role(self, "MANAGER")

    @property
    def is_reportee(self):
        from apps.rbac.client import RBACClient
        return RBACClient().has_role(self, "REPORTEE")
