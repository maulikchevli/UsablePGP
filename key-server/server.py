# flask related imports
from flask import Flask
from flask import jsonify

# other python libs
import sys

app = Flask(__name__)
@app.route('/')
def index():
    return "Key Server"

@app.route('/test_api/<user_id>')
def test(user_id):
    return jsonify({'user_id': user_id})

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
