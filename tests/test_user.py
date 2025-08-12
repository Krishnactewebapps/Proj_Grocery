import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_services():
    with patch('app.routes.user.user_service') as mock_user_service, \
         patch('app.routes.user.auth_service') as mock_auth_service:
        yield mock_user_service, mock_auth_service

def override_get_current_user():
    return {
        'email': 'testuser@example.com',
        'id': 'user123',
        'full_name': 'Test User',
        'bio': 'Test bio',
        'avatar_url': 'http://example.com/avatar.png'
    }

@pytest.fixture(autouse=True)
def override_dependencies():
    with patch('app.routes.user.get_current_user', new=override_get_current_user):
        yield

def test_get_profile_success(mock_services):
    mock_user_service, _ = mock_services
    mock_user = {
        'id': 'user123',
        'email': 'testuser@example.com',
        'full_name': 'Test User',
        'bio': 'Test bio',
        'avatar_url': 'http://example.com/avatar.png'
    }
    mock_user_service.get_user_by_email = AsyncMock(return_value=mock_user)
    response = client.get('/users/me', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'testuser@example.com'
    assert data['id'] == 'user123'
    assert data['full_name'] == 'Test User'
    assert data['bio'] == 'Test bio'
    assert data['avatar_url'] == 'http://example.com/avatar.png'

def test_get_profile_not_found(mock_services):
    mock_user_service, _ = mock_services
    mock_user_service.get_user_by_email = AsyncMock(return_value=None)
    response = client.get('/users/me', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found.'

def test_update_profile_success(mock_services):
    mock_user_service, _ = mock_services
    updated_user = {
        'id': 'user123',
        'email': 'testuser@example.com',
        'full_name': 'Updated User',
        'bio': 'Updated bio',
        'avatar_url': 'http://example.com/avatar2.png'
    }
    mock_user_service.update_user_profile = AsyncMock(return_value=updated_user)
    payload = {
        'email': 'testuser@example.com',
        'full_name': 'Updated User',
        'bio': 'Updated bio',
        'avatar_url': 'http://example.com/avatar2.png'
    }
    response = client.put('/users/me', json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'testuser@example.com'
    assert data['full_name'] == 'Updated User'
    assert data['bio'] == 'Updated bio'
    assert data['avatar_url'] == 'http://example.com/avatar2.png'
    assert data['id'] == 'user123'

def test_update_profile_not_found_or_failed(mock_services):
    mock_user_service, _ = mock_services
    mock_user_service.update_user_profile = AsyncMock(return_value=None)
    payload = {
        'email': 'testuser@example.com',
        'full_name': 'Updated User',
        'bio': 'Updated bio',
        'avatar_url': 'http://example.com/avatar2.png'
    }
    response = client.put('/users/me', json=payload, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found or update failed.'
