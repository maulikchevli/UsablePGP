from flask import request

import os

def get_form_field(field_name):
    if not request.form:
        # Return static for now
        return "dummy"
    elif not field_name in request.form.keys():
        return "dummy"
    else:
        return request.form[field_name]

def save_file(content, name, root):
    with open(os.path.join(root, name), "w") as f:
        f.write(content)

    return os.path.join(root, name)

def get_pr_key():
    return "dummy private key"


def Digest(msg):
    return "Digest of: " + str(msg)

def Encrypt(msg, pu_key):
    return "This msg is encrypted: " + str(msg)

def Signature(msg_digest, pr_key):
    return str(pr_key) + " - Signs - " + str(msg_digest)
