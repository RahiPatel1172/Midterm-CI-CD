from flask import Flask, jsonify, request
from http import HTTPStatus
import math
from functools import wraps, lru_cache
from typing import List, Union
import hashlib
import logging
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def validate_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Validate numeric inputs
            for param in ['num1', 'num2']:
                if param in kwargs:
                    value = kwargs[param]
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"Parameter {param} must be numeric")
            
            # Validate array inputs
            if request.is_json:
                data = request.get_json()
                if 'numbers' in data:
                    if not isinstance(data['numbers'], list):
                        raise ValueError("Numbers must be provided as an array")
                    if not data['numbers']:
                        raise ValueError("Empty array provided")
                    if not all(isinstance(x, (int, float)) for x in data['numbers']):
                        raise ValueError("All array elements must be numeric")
            
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    return wrapper

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/calculate/<int:num1>/<int:num2>')
@limiter.limit("10 per minute")
def calculate(num1, num2):
    try:
        result = {
            'sum': num1 + num2,
            'difference': num1 - num2,
            'product': num1 * num2,
            'quotient': num1 / num2 if num2 != 0 else "Cannot divide by zero",
            'power': math.pow(num1, num2),
            'root': math.pow(num1, 1/num2) if num2 != 0 else "Cannot calculate root with zero",
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

@app.route('/stats', methods=['POST'])
def calculate_stats():
    try:
        data = request.get_json()
        if not data or 'numbers' not in data:
            return jsonify({"error": "Please provide a list of numbers"}), HTTPStatus.BAD_REQUEST
        
        numbers = data['numbers']
        if not numbers or not isinstance(numbers, list):
            return jsonify({"error": "Invalid input format"}), HTTPStatus.BAD_REQUEST

        result = {
            'mean': sum(numbers) / len(numbers),
            'median': sorted(numbers)[len(numbers)//2],
            'min': min(numbers),
            'max': max(numbers),
            'sum': sum(numbers),
            'count': len(numbers)
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

@app.route('/advanced/<operation>', methods=['POST'])
def advanced_operations(operation):
    try:
        data = request.get_json()
        numbers = data.get('numbers', [])
        
        if operation == 'standard_deviation':
            mean = sum(numbers) / len(numbers)
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            result = math.sqrt(variance)
        elif operation == 'factorial':
            result = math.factorial(numbers[0])
        elif operation == 'logarithm':
            base = data.get('base', math.e)
            result = math.log(numbers[0], base)
        else:
            return jsonify({"error": "Unknown operation"}), HTTPStatus.BAD_REQUEST
            
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

@lru_cache(maxsize=1000)
def cached_calculation(operation: str, num1: float, num2: float) -> dict:
    # Perform expensive calculations here
    pass

def cache_key(*args, **kwargs) -> str:
    """Generate a unique cache key for the request"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return hashlib.md5(":".join(key_parts).encode()).hexdigest()

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(
            f"Endpoint: {request.path} | "
            f"Method: {request.method} | "
            f"Duration: {duration}s | "
            f"Status: {result[1] if isinstance(result, tuple) else 200}"
        )
        return result
    return wrapper

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 