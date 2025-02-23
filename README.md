# Midterm Project - Calculator API with CI Pipeline

This project implements a Continuous Integration (CI) pipeline using GitHub Actions for a Flask-based calculator API. The pipeline includes Build, Test, and Docker image upload phases.

## Project Overview

The application is a RESTful API that provides:
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Advanced math operations (power, root)
- Statistical calculations (mean, median, min, max, sum, count)

## Technical Stack
- Python 3.9
- Flask for API development
- pytest for testing
- GitHub Actions for CI/CD
- Docker for containerization

## Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── tests/
│   ├── __init__.py       # Makes tests a Python package
│   └── test_app.py       # Unit tests
└── .github/
    └── workflows/
        └── ci.yml        # GitHub Actions CI pipeline
```

## Features
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Advanced math operations (power, root)
- Statistical calculations (mean, median, min, max, sum, count)
- Standard deviation, factorial, and logarithm calculations
- Rate limiting for API endpoints
- Request logging and monitoring
- Input validation and error handling

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Calculator Operations
```
GET /calculate/<num1>/<num2>
Example: GET /calculate/10/5
Response: {
    "sum": 15,
    "difference": 5,
    "product": 50,
    "quotient": 2,
    "power": 100000,
    "root": 1.5848931924611134
}
```

### Statistical Calculations
```
POST /stats
Body: {"numbers": [1, 2, 3, 4, 5]}
Response: {
    "mean": 3,
    "median": 3,
    "min": 1,
    "max": 5,
    "sum": 15,
    "count": 5
}
```

### Advanced Operations
```
POST /advanced/standard_deviation
Body: {"numbers": [1, 2, 3, 4, 5]}

POST /advanced/factorial
Body: {"numbers": [5]}

POST /advanced/logarithm
Body: {"numbers": [100], "base": 10}
```

## Setup and Installation

1. Clone the repository:
```
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:
```
python app.py
```
The server will start on `http://localhost:5001`

## Running Tests

Execute the test suite:
```
pytest tests/
```

## Docker Support

Build the Docker image:
```bash
docker build -t midterm-calculator .
```

Run the container:
```bash
docker run -p 5001:5001 midterm-calculator
```

## CI Pipeline

The GitHub Actions workflow (`ci.yml`) automates:
- Python environment setup
- Dependency installation
- Unit testing
- Docker image building

The pipeline runs automatically on:
- Push to main branch
- Pull request to main branch

## Rate Limiting

API endpoints are protected with rate limiting:
- Default: 200 requests per day, 50 per hour
- Calculator endpoint: 10 requests per minute

## Error Handling

The API includes comprehensive error handling for:
- Invalid input validation
- Mathematical errors (division by zero)
- Rate limit exceeded
- Server errors

## Monitoring and Logging

- Request logging with timing information
- Endpoint usage monitoring
- Error tracking and reporting

## Notes
- The application runs on port 5001 to avoid conflicts with AirPlay on macOS
- All endpoints return JSON responses
- Error responses include appropriate HTTP status codes