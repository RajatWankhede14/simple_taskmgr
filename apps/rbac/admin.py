from django.contrib import admin
from .models import Policy, Role, RolePermission, UserRole

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "policy", "created_at")
    list_filter = ("role", "policy")

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("user", "role")
