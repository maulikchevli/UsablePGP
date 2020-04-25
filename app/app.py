#! /usr/bin/env python3.7 

# flask related imports
from flask import Flask, request, jsonify, render_template, redirect, url_for

# other python libs
import sys
import requests

from stub import *

app = Flask(__name__)

API_ROUTE = {
    "get_user": "http://localhost:5000/get_user/",
    "insert_users": "http://localhost:5000/insert_users/",
    "test_api" : "http://localhost:5000/test_api/",
}

@app.route('/', methods = ['GET'])
def index():
    """
    Check if the user already has a private key in storage.
    Else, prompt to register.
    """
    return render_template("index.html")

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
        public_key, salt, success = generate_keys(username, pwd)
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

        # Get Private Key
        if to_sign:
            private_key = get_pr_key()
            msg_digest = Digest(msg)

            sign = Signature(msg_digest, private_key)

        # Conditional: two files or one file
        # return AJAX call
        return "Success fully enc/signed"


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
