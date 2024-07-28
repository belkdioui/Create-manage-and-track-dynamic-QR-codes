import re
from django.core.exceptions import ObjectDoesNotExist
from manage_barcode.models import FormData


def check_errors(type, data):
    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    PHONE_REGEX = r"(^(?:05|06|07)\d{8}$|^\+212\d{9}$)"

    errors = {}
    if type=="reset_password":
        if not re.match("^.{8,}$" , data["password"]):
            errors["err_pass"]="password should contain at least 8 characters"
        if not re.match(data["password"], data["cpassword"]):
            errors["err_pass_c"]="password doesn't match confirm password"
    elif type=="sign_up":
        if any(char.isdigit() for char in data["fname"]):
            errors["err_fname"]="First Name invalid "
        if any(char.isdigit() for char in data["lname"]):
            errors["err_lname"]="Last Name invalid "
        if not re.match(EMAIL_REGEX, data["email"]):
            errors["err_email"]="email invalid "
        if not re.match(PHONE_REGEX, data["tel"]):
            errors["err_tel"]="Phone Number invalid "
        if not re.match("^.{8,}$" , data["password"]):
            errors["err_pass"]="password should contain at least 8 characters"
        if not re.match(data["password"], data["cpassword"]):
            errors["err_pass_c"]="password doesn't match confirm password"
        try:
            FormData.objects.get(email=data["email"])
            errors["err_email_ex"] = "email already exists"
        except FormData.DoesNotExist:
            pass

    return errors
