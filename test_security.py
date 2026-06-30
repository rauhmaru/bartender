import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_request_entity_too_large(client):
    """
    Test that a request body larger than MAX_CONTENT_LENGTH (16MB)
    is rejected with a 413 Request Entity Too Large error.
    """
    # Create a payload slightly larger than 16MB
    large_payload = 'A' * (16 * 1024 * 1024 + 1024)

    response = client.post(
        '/cadastrar',
        data={'produto': large_payload, 'tipo': 'Teste', 'volume_ml': '1000'}
    )

    assert response.status_code == 413
