### summary : '

'Validate Credit Card Information'

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
    """

### summary': '

    Use this endpoint to fetch information about a specific BIN (Bank Identification Number).'
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
    """
