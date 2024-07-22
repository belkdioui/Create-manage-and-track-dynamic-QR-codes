    
def check_errors(type, data):
    errors = {}
    if type=="login":
        print("login")
    elif type=="sign_up":
        if any(char.isdigit() for char in data["fname"]):
            errors["err_fname"]="First Name invalid "
        if any(char.isdigit() for char in data["lname"]):
            errors["err_lname"]="Last Name invalid "
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