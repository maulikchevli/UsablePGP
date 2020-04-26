#! /usr/bin/env python3.7 

# flask related imports
from flask import Flask, request, jsonify, render_template, redirect, url_for, \
    send_from_directory, jsonify

# other python libs
import sys
import requests
import os

from utils import *
from stub import *

app = Flask(__name__)

home_dir = os.path.expanduser("~")
app.path = os.path.join(home_dir, ".usablepgp")
app.tmp_path = os.path.join(app.path, "tmp")


API_ROUTE = {
    "get_user": "http://localhost:5000/get_user/",
    "insert_users": "http://localhost:5000/insert_users/",
    "test_api" : "http://localhost:5000/test_api/",
}

# flask routes
@app.route('/', methods = ['GET'])
def index():
    """
    Check if the user already has a private key in storage.
    Else, prompt to register.
    """
    create_app_folder(app)

    registered = False
    if private_key_exists(app.path):
        print("Pr key exists")
        registered = True

    return render_template("index.html", show_register = not registered)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = get_form_field('username')
        pwd = get_form_field('password')

        """
        Generate keys
        """
        public_key, salt, success = generate_keys(username, pwd,
                                                  save_path = app.path)
        if not success:
            # Panic and exit
            sys.exit(-1)

        """
        Call api to store keys
        """
        server_resp = requests.post(
            API_ROUTE['insert_users'],
            json = {
                'username': username,
                'public_key': public_key,
                'salt': salt,
                }
        )

        # TODO .json err control
        if server_resp.json()['status'] == "success":
            return redirect(url_for('index'))
        else:
            # Try again?
            return "Could not add to DB"

@app.route('/enc_sign', methods = ['GET', 'POST'])
def encrypt():
    if request.method == 'GET':
        return render_template("enc_sign.html")
    else:
        msg = get_message_or_file()
        receiver_username = get_form_field('receiver_username')

        # bool values
        ## Check if atleast one is true in JS
        to_enc = get_form_field('to_enc')
        to_sign = get_form_field('to_sign')

        if to_enc:
            receiver_info = get_user_info(receiver_username)
            receiver_pu_key = receiver_info['public_key']

            # DGB
            print(receiver_info, receiver_pu_key)

            msg = Encrypt(msg, receiver_pu_key)
            msg_enc = save_file(msg, 'msg.enc', app.tmp_path)

        # Get Private Key
        if to_sign:
            private_key = get_pr_key()
            msg_digest = Digest(msg)

            sign = Signature(msg_digest, private_key)
            msg_sign = save_file(sign, 'msg.sign', app.tmp_path)

        # return send_from_directory(app.tmp_path, 'msg.enc')

        # return AJAX call
        result = {
            'enc': {'requested': True, 'path': msg_enc},
            'sign': {'requested': False, 'path': msg_sign},
        }
        return jsonify(result)

def get_user_info(username):
    server_resp = requests.get(
        API_ROUTE['get_user'] + str(username)
    )

    # TODO .json err control
    return server_resp.json()


if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )