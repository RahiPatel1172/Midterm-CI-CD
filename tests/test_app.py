import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_calculate_basic_operations(client):
    response = client.get('/calculate/10/5')
    assert response.status_code == 200
    assert response.json['sum'] == 15
    assert response.json['difference'] == 5
    assert response.json['product'] == 50
    assert response.json['quotient'] == 2
    assert response.json['power'] == 100000

def test_calculate_division_by_zero(client):
    response = client.get('/calculate/10/0')
    assert response.status_code == 200
    assert response.json['quotient'] == "Cannot divide by zero"
    assert response.json['root'] == "Cannot calculate root with zero"

def test_stats_calculation(client):
    test_data = {"numbers": [1, 2, 3, 4, 5]}
    response = client.post('/stats',
                         data=json.dumps(test_data),
                         content_type='application/json')
    assert response.status_code == 200
    assert response.json['mean'] == 3
    assert response.json['median'] == 3
    assert response.json['min'] == 1
    assert response.json['max'] == 5
    assert response.json['sum'] == 15
    assert response.json['count'] == 5

def test_stats_invalid_input(client):
    test_data = {"wrong_key": [1, 2, 3]}
    response = client.post('/stats',
                         data=json.dumps(test_data),
                         content_type='application/json')
    assert response.status_code == 400

# This test will fail intentionally
def test_failing_calculation(client):
    response = client.get('/calculate/10/2')
    assert response.status_code == 200
    assert response.json['sum'] == 12, "Sum should be 12, test will fail" 
