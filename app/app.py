#! /usr/bin/env python3.7 

# flask related imports
from flask import Flask, request, jsonify, render_template, redirect, url_for, \
    send_from_directory, jsonify, session

# other python libs
import sys
import requests
import os
import glob
from functools import wraps
from passlib.apps import custom_app_context as passHash

from utils import *
from stub import *

app = Flask(__name__)
app.secret_key = "super secret key"

home_dir = os.path.expanduser("~")
app.root = os.path.join(home_dir, ".usablepgp")

app.path = app.root
app.tmp_path = os.path.join(app.path, "tmp")

API_ROUTE = {
    "get_user": "http://localhost:5000/get_user/",
    "insert_users": "http://localhost:5000/insert_users/",
    "delete_user": "http://localhost:5000/delete_user/",
    "update_public_key": "http://localhost:5000/update_public_key/",
    "test_api" : "http://localhost:5000/test_api/",
}

def update_path(path):
    app.path = path
    app.tmp_path = os.path.join(app.path, "tmp")

def get_user_info(username):
    server_resp = requests.get(
        API_ROUTE['get_user'] + str(username)
    )

    # TODO .json err control
    return server_resp.json()

def create_user_folder(username):
    create_app_folder(os.path.join(app.root, str(username)))
    update_path(os.path.join(app.root, str(username)))
    create_app_folder(app.tmp_path)
    session['username'] = username
    session['logged'] = True

def login_required(f):
	@wraps(f)
	def fn( *args, **kwargs):
		if 'username' not in session:
			#session["flashErr"] = "Please login first!"
			return redirect( url_for('index'))
		return f( *args, **kwargs)
	return fn

def change_path_if_logged(f):
    # Change path if User continues a closed session
    # ie when he reopens app and cookies remain intact
    @wraps(f)
    def fn(*args, **kwargs):
        if 'username' in session:
            update_path(os.path.join(app.root, session['username']))
        return f(*args, **kwargs)
    return fn

# flask routes
@app.route('/', methods = ['GET'])
@change_path_if_logged
def index():

    # TODO Check possible errors if index is not always the first page

    """
    Check if the user already has a private key in storage.
    Else, prompt to register.
    """

    # This should create usablepgp folder at the time of app initialization
    create_app_folder(app.root)

    users = []
    logged = True
    if 'username' not in session:
        logged = False
        user_folders = [ (f.name, f.path) for f in os.scandir(app.root) if f.is_dir() ]
        users = [x[0] for x in user_folders]

    return render_template("index.html", logged=logged, users=users)

@app.route('/login', methods=['POST'])
def login():
    username = get_form_field('username')
    pwd = get_form_field('passphrase')

    user_info = get_user_info(username)
    salt = user_info['salt']

    if not passHash.verify(pwd+salt, user_info['password']):
        session['flash_err'] = "Wrong password"
        return redirect(url_for('index'))

    update_path(os.path.join(app.root, str(username)))
    session['username'] = username
    session['logged'] = True

    session['flash_msg'] = "Welcome, " + str(username) + "! Lets encrypt and stay safe!"
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    update_path(app.root)
    session.pop('username', None)
    session.pop('logged', None)

    session['flash_msg'] = "Logged out"
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = get_form_field('username')
        pwd = get_form_field('password')

        """ Make folder for user
        """
        create_user_folder(str(username))

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
                'password': passHash.hash(pwd+salt),
                'trust': 0,
                }
        )

        # TODO .json err control
        if server_resp.json()['status'] == "success":
            session['flash_msg'] = "Congrats! you created account on our platform."
            return redirect(url_for('index'))
        else:
            # Try again?
            return "Could not add to DB"

@app.route('/enc_sign', methods = ['GET', 'POST'])
@login_required
@change_path_if_logged
def encrypt():
    if request.method == 'GET':
        return render_template("enc_sign.html")
    else:
        msg = get_message_or_file()

        receiver_username = get_form_field('username')
        print(msg, receiver_username)

        # bool values
        ## Check if atleast one is true in JS
        to_enc = get_form_field('encrypt')
        to_sign = get_form_field('sign')

        print(to_enc, to_sign)

        if to_enc:
            receiver_info = get_user_info(receiver_username)
            receiver_pu_key = receiver_info['public_key']

            # DGB
            print(receiver_pu_key)
            enc = Encrypt(msg, receiver_pu_key)

            print(enc)
            enc_f = save_file(enc, 'msg.enc', app.tmp_path)
        else:
            enc = msg
            enc_f = None

        # Get Private Key
        if to_sign:
            sender_info = get_user_info(session['username'])
            pwd = get_form_field('passphrase')

            private_key = get_pr_key(sender_info['username'], app.path)
            salt = sender_info['salt']

            # TODO: Remove print private key
            print(private_key)

            # TODO: remove hard code pwd
            sign = Signature(enc, private_key, pwd, salt)
            print(sign)
            sign_f = save_file(sign, 'msg.sign', app.tmp_path)
        else:
            sign = ""
            sign_f = None

        ## Combine enc and sign
        enc_sign = enc + sign
        enc_sign_f = save_file(enc_sign, 'enc_sign.pgp', app.tmp_path)

        # return AJAX call
        result = {
            'enc': {'requested': True, 'path': enc_f},
            'sign': {'requested': False, 'path': sign_f},
            'enc_sign': {'requested': True, 'path': enc_sign_f}
        }
        #return jsonify(result)
        return send_from_directory(app.tmp_path, 'enc_sign.pgp')

@app.route('/dec_veri', methods = ['GET', 'POST'])
@login_required
@change_path_if_logged
def dec_veri():
    if request.method == 'GET':
        return render_template("dec_ver.html")
    else:
        msg = get_message_or_file()

        to_dec = get_form_field('decrypt')
        to_veri = get_form_field('verify')

        sender_username = get_form_field('username')
        if sender_username:
            sender_info = get_user_info(sender_username)
            sender_pu_key = sender_info['public_key']
        else:
            sender_pu_key = None

        pwd = get_form_field('passphrase')
        if pwd:
            receiver_pr_key = get_pr_key(session['username'], app.path)
            receiver_info = get_user_info(session['username'])
            salt = receiver_info['salt']
        else:
            receiver_pr_key = None
            salt = None

        dec, veri = Decrypt_Verify(to_dec, to_veri, msg, receiver_pr_key, pwd, salt, sender_pu_key)

        if dec:
            dec_f = save_file(dec, "dec.txt", app.tmp_path)
        else:
            dec_f = None

        result = {
            "decryption": dec_f,
            "verification": veri
        }
        return jsonify(result)

@app.route('/revoke_regen', methods = ['GET', 'POST'])
@login_required
@change_path_if_logged
def revoke_regen():
    if request.method == 'GET':
        return render_template("revoke_regen.html")
    else:
        option_selected = get_form_field('revoke_regen')
        pwd = get_form_field('passphrase')
        user_info = get_user_info(session['username'])
        salt = user_info['salt']

        if option_selected == "delete":
            # verify password

            if not passHash.verify(pwd+salt, user_info['password']):
                session['flash_err'] = "Wrong password"
                return redirect(url_for("revoke_regen"))

            # No error checking
            server_resp = requests.delete(
                API_ROUTE['delete_user'],
                json = {
                    'username': session['username']
                }
            )

            import shutil
            shutil.rmtree(app.path)
            logout()

            session['flash_msg'] = "Successfully deleted account"

        # Else regenerate pu key
        else:
            """ This is not rebust.
            One situation is when new private key is generated but api call fails to update in database
            """
            salt = user_info['salt']
            # generate key also saves private key at path
            if not passHash.verify(pwd+salt, user_info['password']):
                session['flash_err'] = "Wrong password"
                return redirect(url_for("revoke_regen"))

            public_key, salt, success = generate_keys(session['username'], pwd,
                                                      save_path = app.path,
                                                      salt = salt)
            if not success:
                # Panic and exit
                sys.exit(-1)

            server_resp = requests.put(
                API_ROUTE['update_public_key'],
                json = {
                    "username": session['username'],
                    "public_key": public_key,
                }
            )

            if server_resp.json()['status'] == "success":
                session['flash_msg'] = "Successfully generated your new key"
            else:
                session['flash_err'] = "Could not connect to our database"

        return redirect(url_for("index"))

@app.route('/key_prop', methods=['GET'])
def key_prop():
    return render_template('key_property.html')

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
