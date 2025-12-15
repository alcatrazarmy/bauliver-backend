"""
Tests for user endpoints.
"""
import pytest
from fastapi import status


def test_get_current_user(client, auth_headers, test_user):
    """Test getting current user profile."""
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["role"] == test_user.role


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication fails."""
    response = client.get("/api/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
