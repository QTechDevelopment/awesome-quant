"""
Unit tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_register_user(client: TestClient, test_user_data: dict):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "password" not in data


@pytest.mark.unit
def test_register_duplicate_user(client: TestClient, test_user_data: dict):
    """Test registering a user with duplicate email."""
    # Register first user
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    # Try to register again with same email
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400


@pytest.mark.unit
def test_login_success(client: TestClient, test_user_data: dict):
    """Test successful login."""
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.unit
def test_login_invalid_credentials(client: TestClient, test_user_data: dict):
    """Test login with invalid credentials."""
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


@pytest.mark.unit
def test_get_current_user(client: TestClient, auth_headers: dict):
    """Test getting current user profile."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "username" in data


@pytest.mark.unit
def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without auth token."""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401


@pytest.mark.unit
def test_refresh_token(client: TestClient, test_user_data: dict):
    """Test refreshing access token."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    tokens = login_response.json()
    
    # Refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
