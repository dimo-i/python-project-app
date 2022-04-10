from django.core.exceptions import ValidationError


import re

VALIDATE_LETTERS_EXCEPTION_MESSAGE = 'Ensure this value contains only letters, numbers, and underscore.'

def validate_letters(value):
    pattern = "^[A-Za-z0-9_-]*$"
    if not re.match(pattern, value):
        raise ValidationError(VALIDATE_LETTERS_EXCEPTION_MESSAGE)