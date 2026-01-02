from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)

    class Meta:
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

class Task(BaseModel):
    class Status(models.TextChoices):
        DEV = "DEV", _("Dev")
        TEST = "TEST", _("Test")
        STUCK = "STUCK", _("Stuck")
        COMP = "COMP", _("Comp")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=Status.choices,
        default=Status.DEV
    )
    categories = models.ManyToManyField(Category, related_name="tasks")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )

    def __str__(self):
        return self.title
