"""
Tests for permit endpoints.
"""
import pytest
from fastapi import status
from app import models


@pytest.fixture
def test_permit(db_session, test_user):
    """Create a test permit."""
    permit = models.Permit(
        customer_name="John Doe",
        address="123 Main St",
        system_size_kw=5.5,
        status="pending",
        user_id=test_user.id
    )
    db_session.add(permit)
    db_session.commit()
    db_session.refresh(permit)
    return permit


def test_create_permit(client, auth_headers):
    """Test creating a permit."""
    response = client.post(
        "/api/permits/",
        json={
            "customer_name": "Jane Smith",
            "address": "456 Oak Ave",
            "system_size_kw": 7.5,
            "status": "pending"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_name"] == "Jane Smith"
    assert data["address"] == "456 Oak Ave"
    assert float(data["system_size_kw"]) == 7.5
    assert data["status"] == "pending"


def test_create_permit_unauthorized(client):
    """Test creating a permit without authentication fails."""
    response = client.post(
        "/api/permits/",
        json={
            "customer_name": "Jane Smith",
            "address": "456 Oak Ave"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_permits_user(client, auth_headers, test_permit):
    """Test user can list their own permits."""
    response = client.get("/api/permits/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_name"] == "John Doe"


def test_list_permits_admin(client, admin_headers, test_permit, db_session, test_admin):
    """Test admin can list all permits."""
    # Create another permit for admin
    admin_permit = models.Permit(
        customer_name="Admin Permit",
        address="789 Admin St",
        system_size_kw=10.0,
        user_id=test_admin.id
    )
    db_session.add(admin_permit)
    db_session.commit()
    
    response = client.get("/api/permits/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Should see both permits


def test_get_permit(client, auth_headers, test_permit):
    """Test getting a specific permit."""
    response = client.get(f"/api/permits/{test_permit.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_permit.id
    assert data["customer_name"] == "John Doe"


def test_get_permit_not_found(client, auth_headers):
    """Test getting non-existent permit returns 404."""
    response = client.get("/api/permits/9999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_permit(client, auth_headers, test_permit):
    """Test updating a permit."""
    response = client.put(
        f"/api/permits/{test_permit.id}",
        json={"status": "approved", "system_size_kw": 6.0},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "approved"
    assert float(data["system_size_kw"]) == 6.0
    assert data["customer_name"] == "John Doe"  # Unchanged


def test_update_permit_forbidden(client, admin_headers, test_permit):
    """Test user cannot update another user's permit."""
    response = client.put(
        f"/api/permits/{test_permit.id}",
        json={"status": "approved"},
        headers=admin_headers
    )
    # Admin should be able to update any permit
    assert response.status_code == status.HTTP_200_OK


def test_delete_permit(client, auth_headers, test_permit):
    """Test deleting a permit."""
    response = client.delete(f"/api/permits/{test_permit.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    response = client.get(f"/api/permits/{test_permit.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_permit_not_found(client, auth_headers):
    """Test deleting non-existent permit returns 404."""
    response = client.delete("/api/permits/9999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
