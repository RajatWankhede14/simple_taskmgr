import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.core.models import Company
from apps.tasks.models import Task
from apps.rbac.client import RBACClient

User = get_user_model()

@pytest.mark.django_db
def test_multi_tenant_isolation():
    """
    Ensures that Manager A cannot see tasks created by Manager B from a different company.
    """
    # 1. Setup Company A and Manager A
    company_a = Company.objects.create(name="Company A", slug="company-a")
    manager_a = User.objects.create_user(
        username="manager_a", 
        email="manager_a@example.com", 
        password="pass", 
        company=company_a
    )
    RBACClient().assign_role(manager_a, "MANAGER")
    
    # 2. Setup Company B and Manager B
    company_b = Company.objects.create(name="Company B", slug="company-b")
    manager_b = User.objects.create_user(
        username="manager_b", 
        email="manager_b@example.com", 
        password="pass", 
        company=company_b
    )
    RBACClient().assign_role(manager_b, "MANAGER")
    
    # 3. Manager B creates a task
    task_b = Task.objects.create(
        title="Secret Task B",
        created_by=manager_b,
        assigned_to=manager_b
    )
    
    # 4. Manager A tries to list tasks
    client = APIClient()
    client.force_authenticate(user=manager_a)
    response = client.get("/api/tasks/")
    
    assert response.status_code == 200
    # Should not see Task B
    assert len(response.data) == 0
    
    # 5. Manager A tries to access Task B directly
    response = client.get(f"/api/tasks/{task_b.id}/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_cross_company_assignment_blocked():
    """
    Ensures a Manager from Company A cannot assign a task to a Reportee in Company B.
    """
    company_a = Company.objects.create(name="Company A", slug="company-a")
    manager_a = User.objects.create_user(
        username="manager_a_2", 
        email="manager_a_2@example.com", 
        password="pass", 
        company=company_a
    )
    RBACClient().assign_role(manager_a, "MANAGER")
    
    company_b = Company.objects.create(name="Company B", slug="company-b")
    reportee_b = User.objects.create_user(
        username="reportee_b", 
        email="reportee_b@example.com", 
        password="pass", 
        company=company_b
    )
    RBACClient().assign_role(reportee_b, "REPORTEE")
    
    client = APIClient()
    client.force_authenticate(user=manager_a)
    
    data = {
        "title": "Cross-company task",
        "assigned_to": reportee_b.id,
        "status": "DEV"
    }
    response = client.post("/api/tasks/", data)
    
    assert response.status_code == 400
    assert "assigned_to" in response.data
    assert "You can only assign tasks to users within your company." in str(response.data["assigned_to"])
