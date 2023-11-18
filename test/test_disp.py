import pytest
from quote_disp.app import app
from unittest.mock import Mock


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'healthy'

def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1  style="color:white; " > This is the Quote Display Service </h1>' in response.data

def test_quote_endpoint(client, mocker):
    """Test the quote endpoint."""
    # Mock the requests.get function to simulate the external service response
    mocker.patch('requests.get', return_value=Mock(text='Test Quote'))

    response = client.get('/get_quote')
    assert response.status_code == 200
    assert b'Test Quote' in response.data

if __name__ == "__main__":
    pytest.main()
