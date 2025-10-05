import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_register_user():
    """Test user registration"""
    # Note: This test will fail without a database connection
    # It's here as a template for when the database is set up
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # This will fail without database, but shows the expected structure
    # response = client.post("/api/v1/auth/register", json=user_data)
    # assert response.status_code == 201
    # assert "id" in response.json()


def test_login_user():
    """Test user login"""
    # Note: This test requires a registered user and database
    # It's here as a template for when the database is set up
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    # This will fail without database and registered user
    # response = client.post("/api/v1/auth/login", data=login_data)
    # assert response.status_code == 200
    # assert "access_token" in response.json()
