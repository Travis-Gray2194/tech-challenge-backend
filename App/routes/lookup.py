import os
import requests
from App.Auth.utils import require_api_key
from flask import Blueprint, jsonify
from flasgger import  swag_from


# Initialize Blueprint for the BIN lookup
bin_lookup_bp = Blueprint('bin_lookup', __name__, url_prefix='/api/v1/lookup')


@bin_lookup_bp.route('/bin-lookup/<bin>', methods=['GET'])

@swag_from({
    'tags': ['BIN Lookup'],
    'summary': 'Use this endpoint to fetch information about a specific BIN (Bank Identification Number).',
    'description':"""
        
        **What is a BIN?**
        A BIN is the first 6-8 digits of a credit or debit card. It identifies the issuing bank or financial institution and provides details about the card type, brand, and other relevant metadata.

        **How to Use:**
        - Pass the BIN as a path parameter in the URL.
        - Example: `/api/v1/lookup/bin-lookup/53319100`.
        - Check the response for details about the BIN, such as the card scheme, issuing bank, and country information.
        
        **Usage Instructions**
        - Set up your environment variables:
        
        - Create a .env file in your project directory and add the following variables:
        - env
        - Copy code
        - X_RAPIDAPI_KEY=your-rapidapi-key
        - X_RAPIDAPI_HOST=bin-ip-checker.p.rapidapi.com
        - CONTENT_TYPE=application/json
        - Run the Flask app:

        **Use the following command to start the server:**
        - bash
        - Copy code
        - python app.py
        - Test the API:

        **Use an HTTP client like Postman or curl to make a GET request:**
        - bash
        - Copy code
        - curl -X GET "http://127.0.0.1:5000/api/v1/lookup/bin-lookup/53319100"
        - View Swagger Documentation:

        Navigate to http://127.0.0.1:5000/apidocs/ to view and interact with the API's Swagger UI.
        
        **Note:** Ensure the BIN you provide is valid and consists of 6-8 digits.
    """,
    
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'The API key required to authenticate the request.',
            'example': 'your-api-key-here'
        },
        {
            'name': 'bin',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The first 6-8 digits of a credit/debit card (BIN/IIN)',
        }
    ],
    'responses': {
        200: {
            'description': 'Successful response with BIN details',
            'examples': {
                'application/json': {
                    "success": True,
                    "data": {
                        "valid": True,
                        "number": "53319100",
                        "length": 8,
                        "scheme": "MasterCard",
                        "brand": "Debit",
                        "type": "Bank",
                        "level": "Standard",
                        "is_commercial": False,
                        "is_prepaid": False,
                        "currency": "USD",
                        "issuer": {
                            "name": "Example Bank",
                            "website": "https://examplebank.com",
                            "phone": "+1-800-1234567"
                        },
                        "country": {
                            "name": "United States",
                            "native": "United States",
                            "flag": "🇺🇸",
                            "numeric": "840",
                            "capital": "Washington D.C.",
                            "currency": "USD",
                            "currency_name": "US Dollar",
                            "currency_symbol": "$",
                            "region": "Americas",
                            "subregion": "Northern America",
                            "idd": "+1",
                            "alpha2": "US",
                            "alpha3": "USA",
                            "language": "English",
                            "language_code": "en"
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid BIN or API response structure',
            'examples': {
                'application/json': {
                    "error": "Invalid API response structure."
                }
            }
        },
        500: {
            'description': 'Internal server error or API request failed',
            'examples': {
                'application/json': {
                    "error": "API request failed: Connection timeout."
                }
            }
        }
    }
})
@require_api_key

def bin_lookup(bin):
    # Define the URL for the API
    url = "https://bin-ip-checker.p.rapidapi.com/"

    
    querystring = {"bin": bin}

    
    headers = {
        "x-rapidapi-key": os.getenv("X_RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("X_RAPIDAPI_HOST"),
        "Content-Type": os.getenv("CONTENT_TYPE"),
    }

    
    try:
        response = requests.post(url, json={"bin": bin}, headers=headers, params=querystring)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500

    
    data = response.json()

    # If the request is successful, format and return the response
    if response.status_code == 200 and "BIN" in data:
        formatted_data = {
            "success": True,
            "code": 200,
            "BIN": {
                "valid": data["BIN"].get("valid"),
                "number": data["BIN"].get("number"),
                "length": data["BIN"].get("length"),
                "scheme": data["BIN"].get("scheme"),
                "brand": data["BIN"].get("brand"),
                "type": data["BIN"].get("type"),
                "level": data["BIN"].get("level"),
                "is_commercial": data["BIN"].get("is_commercial"),
                "is_prepaid": data["BIN"].get("is_prepaid"),
                "currency": data["BIN"].get("currency"),
                "issuer": {
                    "name": data["BIN"]["issuer"].get("name"),
                    "website": data["BIN"]["issuer"].get("website", ""),
                    "phone": data["BIN"]["issuer"].get("phone", "")
                },
                "country": {
                    "name": data["BIN"]["country"].get("name"),
                    "native": data["BIN"]["country"].get("native"),
                    "flag": data["BIN"]["country"].get("flag", ""),
                    "numeric": data["BIN"]["country"].get("numeric"),
                    "capital": data["BIN"]["country"].get("capital"),
                    "currency": data["BIN"]["country"].get("currency"),
                    "currency_name": data["BIN"]["country"].get("currency_name"),
                    "currency_symbol": data["BIN"]["country"].get("currency_symbol"),
                    "region": data["BIN"]["country"].get("region"),
                    "subregion": data["BIN"]["country"].get("subregion"),
                    "idd": data["BIN"]["country"].get("idd"),
                    "alpha2": data["BIN"]["country"].get("alpha2"),
                    "alpha3": data["BIN"]["country"].get("alpha3"),
                    "language": data["BIN"]["country"].get("language"),
                    "language_code": data["BIN"]["country"].get("language_code")
                }
            }
        }


        return jsonify(formatted_data), 200
    else:
        return jsonify({"error": data.get('error', 'Unable to fetch BIN details.')}), 400
