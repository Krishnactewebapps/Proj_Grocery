import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

# Use TestClient for FastAPI
client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_services():
    with patch('app.routes.auth.user_service') as mock_user_service, \
         patch('app.routes.auth.auth_service') as mock_auth_service:
        yield mock_user_service, mock_auth_service

def test_register_user_success(mock_services):
    mock_user_service, _ = mock_services
    mock_user = {
        'id': '123',
        'email': 'test@example.com',
        'full_name': 'Test User',
        'bio': None,
        'avatar_url': None
    }
    mock_user_service.create_user = AsyncMock(return_value=mock_user)
    payload = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'password1234'
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'test@example.com'
    assert data['full_name'] == 'Test User'
    assert data['id'] == '123'

def test_register_user_already_exists(mock_services):
    mock_user_service, _ = mock_services
    mock_user_service.create_user = AsyncMock(return_value=None)
    payload = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'password1234'
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 400
    assert response.json()['detail'] == 'User already exists or invalid data.'

def test_login_user_success(mock_services):
    _, mock_auth_service = mock_services
    mock_auth_service.authenticate_user = AsyncMock(return_value='fake-jwt-token')
    payload = {
        'email': 'test@example.com',
        'password': 'password1234'
    }
    response = client.post('/auth/login', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['access_token'] == 'fake-jwt-token'
    assert data['token_type'] == 'bearer'

def test_login_user_invalid_credentials(mock_services):
    _, mock_auth_service = mock_services
    mock_auth_service.authenticate_user = AsyncMock(return_value=None)
    payload = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/auth/login', json=payload)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials.'
