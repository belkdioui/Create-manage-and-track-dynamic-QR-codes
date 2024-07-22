import re

def check_errors(type, data):
    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    PHONE_REGEX = r"(^(?:05|06|07)\d{8}$|^\+212\d{9}$)"

    errors = {}
    if type=="login":
        print("login")
    elif type=="sign_up":
        if any(char.isdigit() for char in data["fname"]):
            errors["err_fname"]="First Name invalid "
        if any(char.isdigit() for char in data["lname"]):
            errors["err_lname"]="Last Name invalid "
        if not re.match(EMAIL_REGEX, data["email"]):
            errors["err_email"]="email invalid "
        if not re.match(PHONE_REGEX, data["tel"]):
            errors["err_tel"]="Phone Number invalid "
    return errors
    # def check_register(data):
    #     def check_if_emaail_is_valdi(email):
    #         pass
    
    # def check_login(data):
    #     pass


    # if type == "register":
    #     check_register(data)
    # elif type == "login":
    #     check_login(data)