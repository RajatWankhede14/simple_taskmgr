import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user_with_email():
    user = User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="password123"
    )
    assert user.username == "test@example.com"
    assert user.email == "test@example.com"
    assert user.is_active

@pytest.mark.django_db
def test_create_user_with_mobile():
    user = User.objects.create_user(
        username="1234567890",
        mobile="1234567890",
        password="password123"
    )
    assert user.username == "1234567890"
    assert user.mobile == "1234567890"
    assert user.is_active

@pytest.mark.django_db
def test_soft_delete():
    user = User.objects.create_user(
        username="delete_me",
        password="password123"
    )
    user.delete()
    assert User.objects.filter(username="delete_me").count() == 0
    assert User.all_objects.filter(username="delete_me").count() == 1
    assert User.all_objects.get(username="delete_me").deleted_at is not None

@pytest.mark.django_db
def test_create_superuser():
    admin_user = User.objects.create_superuser(
        username="admin",
        password="password123"
    )
    assert admin_user.username == "admin"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
