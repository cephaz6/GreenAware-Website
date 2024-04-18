from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def validate_email_address(email):
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Invalid email address.')
        return redirect("/register")
