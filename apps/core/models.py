from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, hard=False, **kwargs):
        if hard:
            super().delete(**kwargs)
        else:
            self.deleted_at = now()
            self.save()

    def hard_delete(self):
        self.delete(hard=True)

class Company(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
