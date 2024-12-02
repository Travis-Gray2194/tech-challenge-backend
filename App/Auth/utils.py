from flask import request, jsonify, Blueprint
from flasgger import  swag_from
import os

secure_bp = Blueprint('secure', __name__, url_prefix='/api/v1/secure_bp')

# # Load the API key from the environment
API_KEY = os.getenv("API_KEY")

def require_api_key(func):
    """
    Decorator to require an API key for accessing a route.
    """
    def wrapper(*args, **kwargs):
        # Retrieve API key from the request header
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized access, invalid API key"}), 401
        return func(*args, **kwargs)
    return wrapper


@secure_bp.before_request
def check_api_key():
    """
    Check API key for all routes in this blueprint.
    """
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized access, invalid API key"}), 401
    

@secure_bp.route("/info", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key required for access to the protected route.',
        }
    ],
    'responses': {
        '200': {
            'description': 'Info retrieved successfully',
            'examples': {
                'application/json': {'info': 'This is a protected route.'}
            }
        },
        '401': {
            'description': 'Unauthorized access'
        }
    }
}) 
def info():
    return jsonify({"info": "This is a protected route."})