from django.contrib.auth import get_user_model
from apps.tasks.models import Task, Category
from apps.authentication.models import User
import pytest

@pytest.mark.django_db
def test_task_refinements():
    # 0. Create Company
    from apps.core.models import Company
    company = Company.objects.create(name="Test Corp", slug="test-corp")

    # 1. Create Manager
    manager = User.objects.create_user(
        username="manager1",
        email="manager1@example.com",
        password="password123",
        company=company
    )
    from apps.rbac.client import RBACClient
    RBACClient().assign_role(manager, "MANAGER")
    assert manager.is_manager

    # 2. Create Reportee
    reportee = User.objects.create_user(
        username="reportee1",
        email="reportee1@example.com",
        password="password123",
        company=company
    )
    RBACClient().assign_role(reportee, "REPORTEE")
    assert reportee.is_reportee

    # 3. Create Categories
    cat1 = Category.objects.create(name="Frontend")
    cat2 = Category.objects.create(name="Urgent")

    # 4. Manager creates task with categories
    task = Task.objects.create(
        title="Refine UI",
        assigned_to=reportee,
        created_by=manager,
        status=Task.Status.DEV
    )
    task.categories.add(cat1, cat2)

    assert task.status == "DEV"
    assert task.categories.count() == 2
    assert task.created_by == manager
    assert task.assigned_to == reportee

    # 5. Test Status Update (COMP)
    task.status = Task.Status.COMP
    task.save()
    assert task.status == "COMP"
