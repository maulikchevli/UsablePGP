# flask related imports
from flask import Flask

# other python libs
import sys

app = Flask(__name__)
@app.route('/')
def index():
    return "User Inerface controller"

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    app.run(
        host = host,
        port = port,
        debug = True
    )
