# Secure Multi-Tenant Task Management System

A robust, multi-tenant Django REST Framework application for task management with enterprise-grade RBAC and API abuse prevention.

## 🏗 Data Model Explanation

The system is built on a modular architecture using the following core entities:

### 🏢 Core & Multi-Tenancy
- **Company**: Represents a tenant. All users and tasks belong to a specific company.
- **BaseModel**: An abstract base class providing `created_at`, `updated_at`, and `deleted_at` fields for auditing and soft-deletion across all tables.

### 🔐 Identity & Access
- **User**: Custom user model supporting email/mobile as identifiers. Linked to a `Company`.
- **Role**: Defines specialized roles (`MANAGER`, `REPORTEE`).
- **UserRole**: Maps users to roles, allowing for future-proof multiple role assignments per user.
- **Policy**: High-level permission definitions.
- **RolePermission**: Maps roles to specific policies.

### 📝 Task Management
- **Category**: Labels for grouping tasks (e.g., Frontend, Backend, Urgent).
- **Task**: The primary work unit. Contains title, description, and status (`DEV`, `TEST`, `STUCK`, `COMP`). Tasks are linked to a creator (Manager) and an assignee (Reportee).

---

## 🛡 Role-Based Permission Logic

Permissions are enforced at the API layer using custom DRF `BasePermission` classes:

- **Managers**:
    - Full CRUD access to tasks created within their company.
    - Ability to create and manage Reportee accounts for their company.
- **Reportees**:
    - Read-only access to tasks specifically assigned to them.
    - Status updates are restricted: **Reportees can only transition tasks to the `COMP` (Completed) status.** Any other transition attempt is rejected by the serializer.

---

## 🏢 Company-Level Data Isolation Strategy

Isolation is achieved through a multi-layered approach:
1.  **Strict Relationships**: Every user is pinned to a `Company` at signup/creation.
2.  **Manager Constraint**: Reportees created by a Manager automatically inherit that Manager's `Company`.
3.  **Queryset Filtering**: The `TaskViewSet` overrides `get_queryset` to ensure users only see tasks within their organizational scope:
    - **Managers**: Can see all tasks created by any user in their `Company`.
    - **Reportees**: Can only see tasks specifically assigned to them.
4.  **Ownership & Assignment Validation**: 
    - The `perform_create` hook automatically sets `created_by` to the current Manager.
    - Serializer validation blocks Managers from assigning tasks to users outside their `Company`.

---

## 🚦 Rate-Limiting Approach and Trade-offs

The system implements a **Token Bucket (Bucket Pattern)** algorithm for precise control:

### Approach
- **Per-IP Limits**: Protects against brute-force and DDoS from unauthenticated clients.
- **Per-User Limits**: Prevents authenticated users from overwhelming the system or scraping data.
- **Specialized Scopes**: Different rates for `auth` (very strict), `task_create` (strict), and `task_list` (relaxed).

### Trade-offs
- **Complexity vs. Precision**: The Token Bucket is more complex than fixed-window limiting but allows for "burstiness" (handling a few rapid clicks) while maintaining a strict long-term average.
- **Storage**: State (tokens and timestamp) is stored in the cache. Using the database for this would be too slow, so a fast cache (like Redis) is recommended for production.

---

## 🚀 Setup Instructions

### Local Development

1.  **Install dependencies**:
    ```bash
    make install
    ```
2.  **Apply migrations**:
    ```bash
    make migrate
    ```
3.  **Seed initial roles**:
    ```bash
    python manage.py shell -c "from apps.rbac.models import Role; Role.objects.get_or_create(name='MANAGER'); Role.objects.get_or_create(name='REPORTEE')"
    ```
4.  **Run the server**:
    ```bash
    make run
    ```
5.  **Access API Docs**: Open `http://localhost:8000/api/docs/` for Swagger documentation.

---

## ✨ Possible Improvements

1.  **Explicit Multi-Tenant Middleware**: Implementing a middleware that sets a `company_id` on the request globally would simplify filtering in complex queries (e.g., using `django-multitenant`).
2.  **Explicit Company field on Task**: Adding a direct ForeignKey from `Task` to `Company` for even faster indexing and simpler cross-filtering if Managers need to see tasks they didn't create but belong to their company.
3.  **Notification System**: Integrated signals to notify Reportees via email/mobile when a task is assigned.

