# flask related imports
from flask import Flask
from flask import jsonify
from flask import request

# other python libs
import sys

app = Flask(__name__)
@app.route('/')
def index():
    return "Key Server"

@app.route('/test_api/', methods = ['POST'])
def test():
    tmp = request.get_json()
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
