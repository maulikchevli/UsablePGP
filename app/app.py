# flask related imports
from flask import Flask, request, jsonify

# other python libs
import sys
import requests

from stub import *

app = Flask(__name__)

API_ROUTE = {
    "test_api" : "http://localhost:5000/test_api/"
}

@app.route('/', methods = ['GET'])
def index():
    return "User Interface controller"

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        return render_template("register.html")
    else:
        user_id = get_form_field('user_id')
        pwd = get_form_field('pwd')

        """
        Generate keys
        """
        success = generate_keys(user_id, pwd)
        if not success:
            # Panic and exit
            sys.exit(-1)

        """
        Call api to store keys
        """
        server_resp = requests.post(
            API_ROUTE['test_api'],
            json = {'user_id': user_id}
        )

        if server_resp.json()['status'] == "success":
            return "Render Home screen"
        else:
            # Try again?
            return "Could not add to DB"

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
