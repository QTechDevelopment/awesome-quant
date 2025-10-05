"""
Pytest configuration and fixtures.
"""
import pytest
import asyncio
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.core.config import get_settings


settings = get_settings()

# Test database URL
TEST_DATABASE_URL = "postgresql://speedtrade:password@localhost:5432/speedtrade_test"

# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user registration data."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }


@pytest.fixture
def auth_headers(client: TestClient, test_user_data: dict):
    """Get authentication headers for a test user."""
    # Register user
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == 200
    
    token_data = response.json()
    return {"Authorization": f"Bearer {token_data['access_token']}"}
