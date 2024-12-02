import re

def validate_card_type(card_number):
    """Determines the card type based on prefix and length."""
    card_number = str(card_number)
    if re.match(r'^4\d{12}(\d{3})?$', card_number):
        return "Visa"
    elif re.match(r'^5[1-5]\d{14}$', card_number):
        return "MasterCard"
    elif re.match(r'^6(?:011|5\d{2})\d{12}$', card_number):
        return "Discover"
    elif re.match(r'^3[47]\d{13}$', card_number):
        return "American Express"
    elif re.match(r'^3(?:0[0-5]|[68]\d)\d{11}$', card_number):
        return "Diners Club"
    elif re.match(r'^(?:2131|1800|35\d{3})\d{11}$', card_number): #JCB
        return "JCB"
    else:
        return None

def luhn_algorithm(card_number):
    """Implements the Luhn algorithm for card validation."""
    digits = [int(d) for d in str(card_number)][::-1]
    checksum = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            doubled = digit * 2
            checksum += doubled if doubled < 10 else doubled - 9
        else:
            checksum += digit
    return checksum % 10 == 0


def validate_cvv(card_number, cvv):
    """Validates the CVV based on the card type."""
    if not cvv.isdigit():
        return False

    card_type = validate_card_type(card_number)
    if card_type == "American Express" and len(cvv) == 4:
        return True
    elif card_type in ["Visa", "MasterCard", "Discover"] and len(cvv) == 3:
        return True
    return False


def mask_credit_card(card_number):
    """Mask the credit card number except for the last 4 digits."""
    return "**** **** **** " + card_number[-4:]

def mask_sensitive_data(data):
    """Mask sensitive information in the given data (like card number, CVV, etc.)."""
    if 'card_number' in data:
        data['card_number'] = mask_credit_card(data['card_number'])
    if 'cvv' in data:
        data['cvv'] = "****"
    return data
