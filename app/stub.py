from flask import request

def generate_keys(user_id, pwd):
    return "test pu key", 1111, True

def get_form_field(field_name):
    if not request.form:
        # Return static for now
        return "u16co"
    else:
        return request.form[field_name]

