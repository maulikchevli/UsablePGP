#! /usr/bin/env python3.7 

# flask related imports
from flask import Flask, request, jsonify, render_template, redirect, url_for

# other python libs
import sys
import requests

from stub import *

app = Flask(__name__)

API_ROUTE = {
    "test_api" : "http://localhost:5000/test_api/",
    "insert_users": "http://localhost:5000/insert_users/",
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

@app.route('/encrypt')
def encrypt():
    return render_template("encrypt.html")


if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
