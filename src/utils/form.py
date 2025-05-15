"""
Input validator.
"""

# Standard library
import re


__schema = {
    'name': {
        'type': str,
        'required': True
    },
    'email': {
        'type': str,
        'required': True,
        'regex': r'^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,6}$'
    },
    'phone': {
        'type': str,
        'required': True,
        'regex': r'^\+[0-9]+$'
    },
    'username': {
        'type': str,
        'minlength': 8,
        'maxlength': 16,
        'required': True,
        'regex': r'^[a-z0-9]{8,16}$',
        'custom': lambda value: (
            any(char.isdigit() for char in value) and
            any(char.islower() for char in value)
        ) or (
            'Usernname must contain at least one number, '
            'and lowercase letter.'
        )
    },
    'password': {
        'type': str,
        'minlength': 8,
        'maxlength': 16,
        'required': True,
        'regex': r'^[a-zA-Z0-9@$#^*]{8,16}$',
        'custom': lambda value: (
            any(char.isdigit() for char in value) and
            any(char.isupper() for char in value) and
            any(char.islower() for char in value)
        ) or (
            'Password must contain at least one number, '
            'one uppercase letter, and one lowercase letter.'
        )
    }
}

def validate(data):
    """
    Validate form input against predefined schema rules.

    The function checks if the given `data` dictionary contains valid values based
    on the rules defined in the `__schema` for each field. The schema includes
    checks for type, required fields, minimum and maximum length, regex pattern
    matching, and custom validation logic.

    Args:
        data (dict): A dictionary of form data where keys are field names and
        values are user-provided input.

    Returns:
        tuple:
            - bool: `True` if all fields are valid, `False` if there are any
            validation errors.
            - dict: A dictionary of errors where the key is the field name and
            the value is the error message.

    Schema Validation Rules:
        1. `required` (bool): Whether the field is mandatory.
        2. `type` (type): Expected data type (e.g., `str` for strings).
        3. `minlength` (int): Minimum allowed length of the value.
        4. `maxlength` (int, optional): Maximum allowed length of the value.
        5. `regex` (str, optional): Regular expression to match the field value.
        6. `custom` (function, optional): Custom validation logic that checks
           specific field rules. It should return either `True` (valid) or an
           error message string.

    Example Usage:
        data = {
            'email': 'user@example.com',
            'password': 'StrongP@ssw0rd'
        }

        is_valid, errors = validate(data)

        if is_valid:
            print("All fields are valid")
        else:
            print("Errors found:", errors)
    """
    errors = {}

    for field,value in data.items():
        rules = __schema[field]
        errors[field] = []
        # Check if field is required and missing
        if rules['required'] and value is None:
            del errors[field]
            errors[field] = f"{field.capitalize()} is required."
            continue

        # Check type
        if 'type' in rules and not isinstance(value, rules['type']):
            errors[field].append(f"{field.capitalize()} must be a {rules['type']}")

        # Check minlength
        if 'minlength' in rules and len(value) < rules['minlength']:
            errors[field].append((
                f"{field.capitalize()} must be at least "
                f"{rules['minlength']} characters long."
            ))

        # Check maxlength
        if 'maxlength' in rules and len(value) > rules['maxlength']:
            errors[field].append((
                f"{field.capitalize()} cannot be more than "
                f"{rules['maxlength']} characters long."
            ))

        # Check custom validation
        if 'custom' in rules and rules['custom']:
            custom_error = rules['custom'](value)
            if custom_error is not True:
                errors[field].append(custom_error)

        if len(errors[field]) > 0:
            errors[field] = '\n'.join(errors[field])
            continue

        del errors[field]

        # Check regex
        if 'regex' in rules:
            if not re.match(rules['regex'], value):
                errors[field] = f"Invalid {field.capitalize()}"

    return not bool(errors), errors
