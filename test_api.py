import requests
import json

BASE_URL = "http://localhost:5001"

def test_all_endpoints():
    # Test health check
    response = requests.get(f"{BASE_URL}/health")
    print("Health check:", response.json())

    # Test calculator
    response = requests.get(f"{BASE_URL}/calculate/10/5")
    print("\nCalculator (10/5):", json.dumps(response.json(), indent=2))

    # Test division by zero
    response = requests.get(f"{BASE_URL}/calculate/10/0")
    print("\nDivision by zero:", json.dumps(response.json(), indent=2))

    # Test stats
    data = {"numbers": [1, 2, 3, 4, 5]}
    response = requests.post(f"{BASE_URL}/stats", json=data)
    print("\nStats calculation:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_all_endpoints() 