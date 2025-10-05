"""
Unit tests for portfolio endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from decimal import Decimal


@pytest.mark.unit
def test_get_portfolio(client: TestClient, auth_headers: dict):
    """Test getting portfolio summary."""
    response = client.get("/api/v1/portfolio", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "cash_balance" in data
    assert "total_equity" in data
    assert "unrealized_pnl" in data
    assert "realized_pnl" in data


@pytest.mark.unit
def test_get_portfolio_unauthorized(client: TestClient):
    """Test getting portfolio without authentication."""
    response = client.get("/api/v1/portfolio")
    
    assert response.status_code == 401


@pytest.mark.unit
def test_get_positions(client: TestClient, auth_headers: dict):
    """Test getting open positions."""
    response = client.get("/api/v1/portfolio/positions", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "positions" in data
    assert "total" in data
    assert isinstance(data["positions"], list)


@pytest.mark.unit
def test_get_positions_filter_by_asset_type(client: TestClient, auth_headers: dict):
    """Test filtering positions by asset type."""
    response = client.get(
        "/api/v1/portfolio/positions?asset_type=stock",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "positions" in data
