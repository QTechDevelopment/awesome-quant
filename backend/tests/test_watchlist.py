import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_watchlist_endpoints_exist():
    """Test that watchlist endpoints are registered"""
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    
    assert '/api/v1/watchlist/' in routes
    assert '/api/v1/watchlist/{watchlist_id}' in routes
    assert '/api/v1/watchlist/{watchlist_id}/items' in routes


def test_buy_endpoints_exist():
    """Test that buy endpoints are registered"""
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    
    assert '/api/v1/orders/buy' in routes
    assert '/api/v1/orders/queue-buy' in routes
