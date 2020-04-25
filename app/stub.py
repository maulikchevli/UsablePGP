from flask import request

def generate_keys(user_id, pwd):
    return "test pu key", 1111, True

def get_form_field(field_name):
    if not request.form:
        # Return static for now
        return "dummy"
    else:
        return request.form[field_name]

def get_message_or_file():
    return "Test Message"

def get_pr_key():
    return "dummy private key"

# pgp functions
def Digest(msg):
    return "Digest of: " + str(msg)

def Encrypt(msg, pu_key):
    return "This msg is encrypted: " + str(msg)

def Signature(msg_digest, pr_key):
    return str(pr_key) + " - Signs - " + str(msg_digest)
