# flask related imports
from flask import Flask
from flask import jsonify
from flask import request,abort


# other python libs
import sys
import sqlite3 as sql


def dict_factory(cursor,row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

app = Flask(__name__)
@app.route('/')
def index():
    return "Key Server"

@app.route('/test_api/', methods = ['POST'])
def test():
    tmp = request.get_json()
    return jsonify({'status': 'success'})

@app.route('/insert_users/',methods=['POST'])
def insert_users():
    if not request.json or not 'username' in request.json:
        print('aborted')
        abort(400)

    username = request.json['username']
    password = request.json['password']
    public_key = request.json['public_key']
    salt = request.json['salt']
    trust = 0
    signature = ""

    status = "failure"
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if users:
            status = "failure"
        else:
            print("inserting")
            cur.execute("INSERT INTO users (username,password,public_key,salt,trust,signature) VALUES (?,?,?,?,?,?)",(str(username),str(password),str(public_key),str(salt),str(trust),str(signature)))
            print("inserted")
            con.commit()
            print("comitted")
            status = "success"
    return jsonify({'status':status})

@app.route('/get_user/<username>',methods=['GET'])
def get_user(username):
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if not users:
            abort(404)
        else:
            user = {
                'username': users[0]['username'],
                'password': users[0]['password'],
                'public_key':users[0]['public_key'],
                'salt':users[0]['salt'],
                'trust':users[0]['trust'],
                'signature':users[0]['signature']
            }
            return jsonify(user)

@app.route('/get_users/',methods=["GET"])
def get_users():
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        users_json = {
            "users":[]
        }
        for user in users:
            user_json = {
                'username': user['username'],
                'public_key':user['public_key'],
                'salt':user['salt'],
                'trust':user['trust'],
                'signature':user['signature']
            }
            users_json["users"].append(user_json)
        return jsonify(users_json)

@app.route('/update_public_key/',methods=["PUT"])
def update_public_key():
    if not request.json or not 'username' in request.json:
        abort(404)

    username = request.json["username"]
    public_key = request.json["public_key"]
    status = "failure"
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if not users:
            status = "failure"
        else:
            print("updating")
            cur.execute("UPDATE users SET public_key=? WHERE username=?",(str(public_key),str(username),))
            print("updated")
            con.commit()
            print("comitted")
            status = "success"
    return jsonify({'status':status})

@app.route('/update_salt/',methods=["PUT"])
def update_salt():
    if not request.json or not 'username' in request.json:
        abort(404)

    username = request.json["username"]
    salt = request.json["salt"]
    status = "failure"
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if not users:
            status = "failure"
        else:
            print("updating")
            cur.execute("UPDATE users SET salt=? WHERE username=?",(str(salt),str(username),))
            print("updated")
            con.commit()
            print("comitted")
            status = "success"
    return jsonify({'status':status})

@app.route('/update_trust/',methods=["PUT"])
def update_trust():
    if not request.json or not 'username' in request.json:
        abort(404)

    username = request.json["username"]
    trust = 1
    signature = request.json["signature"]
    status = "failure"
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if not users:
            status = "failure"
        else:
            print("updating")
            cur.execute("UPDATE users SET trust=?,signature=? WHERE username=?",(trust,str(signature),str(username),))
            print("updated")
            con.commit()
            print("comitted")
            status = "success"
    return jsonify({'status':status})

@app.route('/delete_user/',methods=["DELETE"])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(404)

    username = request.json["username"]

    status = "failure"
    with sql.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username=?",(str(username),))
        users = cur.fetchall()

        if not users:
            status = "failure"
        else:
            print("deleting")
            cur.execute("DELETE FROM users WHERE username=?",(str(username),))
            print("deleted")
            con.commit()
            print("comitted")
            status = "success"
    return jsonify({'status':status})

if __name__ == "__main__":
    app.run(
        host = "localhost",
        port = 5000,
    )
