from flask import Blueprint, request, jsonify
from datetime import datetime
from App.validate import *
from flasgger import swag_from
from App.Auth.utils import require_api_key

# Define the Blueprint for validation routes
validation_bp = Blueprint('validation', __name__, url_prefix='/api/v1/card_validation')


@validation_bp.route('/validate', methods=['POST'])
@swag_from({
    'tags': ['Credit Card Validation'],
    'summary': 'Validate Credit Card Information',
    'description': """
        Validate credit card details including:
        - **Card Number:** The 16-digit card number.
        - **Expiration Date:** Expiry date in MM/YY format.
        - **CVV:** 3-digit security code on the back of the card.

        ### Example Request
        ```json
        {
            "card_number": "4834851062286956",
            "expiration_date": "10/27",
            "cvv": "848"
        }
        ```

        ### Response
        - **200:** Card details are valid.
        - **400:** Invalid input (e.g., wrong format, invalid data).
        - **500:** Server error during validation.

        ### Endpoint: /api/v1/card_validation/validate
          **Method**: POST
          **Request Body**
          - The API expects a POST request with a JSON body containing the following fields:

          - card_number (string): The full 16-digit credit card number.
          - expiration_date (string): The card's expiration date in MM/YY format.
          - cvv (string): The 3-digit CVV (Card Verification Value).

        **Note:** Ensure the card details follow standard formatting rules.
          - The validation checks whether the card number is valid according to the Luhn algorithm, the expiration date is not expired, and the CVV matches the expected value for the card type.
            Make sure to format the data correctly, especially the expiration date (MM/YY) and the CVV (3 digits).
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
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'card_number': {
                        'type': 'string',
                        'description': 'The full 16-digit credit card number.',
                        'example': '4834851062286956'
                    },
                    'expiration_date': {
                        'type': 'string',
                        'description': 'The card\'s expiration date in MM/YY format.',
                        'example': '10/27'
                    },
                    'cvv': {
                        'type': 'string',
                        'description': 'The 3-digit CVV (Card Verification Value) from the back of the card.',
                        'example': '848'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Validation succeeded.',
            'examples': {
                'application/json': {
                    "card_number": "4834851062286596",
                    "card_type": "Visa",
                    "is_valid_luhn": True,
                    "expiration_date": "10/27",
                    "is_valid_expiration": True,
                    "cvv": "048",
                    "is_valid_cvv": True,
                    "valid_card_data": True
                }
            }
        },
        400: {
            'description': 'Validation failed.',
            'examples': {
                'application/json': {
                    "error": "Invalid expiration date format. Expected MM/YY"
                }
            }
        },
        500: {
            'description': 'Server error.',
            'examples': {
                'application/json': {
                    "error": "Internal server error during validation."
                }
            }
        }
    }
})
@require_api_key
def validate_card_expiration_cvv():
    """
    Validate credit card details including:
    - Card number (Luhn check)
    - Expiration date (MM/YY format)
    - CVV (Card Verification Value)
    """
    data = request.json

    card_number = data.get("card_number")
    expiration_date = data.get("expiration_date")
    cvv = data.get("cvv")

    if not card_number or not card_number.isdigit():
        return jsonify({"error": "Invalid card number provided"}), 400

    if not expiration_date:
        return jsonify({"error": "Expiration date is required"}), 400

    try:
        exp_date = datetime.strptime(expiration_date, "%m/%y")
        is_valid_expiration = exp_date > datetime.now()
    except ValueError:
        return jsonify({"error": "Invalid expiration date format. Expected MM/YY"}), 400

    if not cvv or not validate_cvv(card_number, cvv):
        return jsonify({"error": "Invalid CVV provided for the given card type"}), 400

    card_type = validate_card_type(card_number)
    is_valid_luhn = luhn_algorithm(card_number)

    log_data = {
        "card_number": card_number,
        "expiration_date": expiration_date,
        "cvv": cvv,
        "is_valid_luhn": is_valid_luhn,
        "is_valid_expiration": is_valid_expiration,
        "card_type": card_type
    }
    mask_sensitive_data(log_data)

    if is_valid_luhn and is_valid_expiration and validate_cvv(card_number, cvv):
        return jsonify({
            "card_number": mask_credit_card(card_number),
            "card_type": card_type,
            "is_valid_luhn": is_valid_luhn,
            "expiration_date": expiration_date,
            "is_valid_expiration": is_valid_expiration,
            "cvv": "****",
            "is_valid_cvv": True,
            "valid_card_data": True
        }), 200
    else:
        return jsonify({
            "card_number": mask_credit_card(card_number),
            "card_type": card_type,
            "is_valid_luhn": is_valid_luhn,
            "expiration_date": expiration_date,
            "is_valid_expiration": is_valid_expiration,
            "cvv": "****",
            "is_valid_cvv": False,
            "valid_card_data": False
        }), 400