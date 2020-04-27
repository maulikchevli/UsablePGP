from flask import request

import os

def get_form_field(field_name):
    if not request.form:
        # Return static for now
        return "dummy"
    elif not field_name in request.form.keys():
        return None
    else:
        return request.form[field_name]

