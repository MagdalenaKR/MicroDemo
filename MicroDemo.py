from flask import Flask
from flask import make_response
from flask import request
from flask import abort
from flask import jsonify
import json
import sqlite3

app = Flask(__name__)


def connectToDB():
    connection = sqlite3.connect('C:\sqlite\mydb.sqlite')
    print("Open DB successfully!")
    return connection


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/info')
def home_index():
    conn = connectToDB()
    api_list = []
    cursor = conn.execute("SELECT buildtime,version,methods,links FROM apirelease")
    for row in cursor:
        a_dict = {}
        a_dict['version'] = row[1]
        a_dict['buildtime'] = row[0]
        a_dict['methods'] = row[2]
        a_dict['links'] = row[3]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'api_version': api_list}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


def list_users():
    conn = connectToDB()
    api_users = []
    cursor = conn.execute('SELECT username,emailid, password, full_name,id FROM users')

    for item in cursor:
        api_udisct = {}
        api_udisct['username'] = item[0]
        api_udisct['emailid'] = item[1]
        api_udisct['password'] = item[2]
        api_udisct['full_name'] = item[3]
        api_udisct['id'] = item[4]
        api_users.append(api_udisct)

    conn.close()
    return jsonify({'users_list': api_users}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


def list_user(user_id):
    conn = connectToDB()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    data = cursor.fetchall()
    users = {}
    if len(data) != 0:

        users['username'] = data[0][0]
        users['emailid'] = data[0][1]
        users['password'] = data[0][2]
        users['full_name'] = data[0][3]
        users['id'] = data[0][4]
        conn.close()
        return jsonify(users)
    else:
        conn.close()
        abort(404)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
    api_list = []
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=? or emailid =?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username, emailid, password,full_name) values(?, ?, ?, ?)",(new_user['username'],new_user['email'],new_user['password'], new_user['name']))
    conn.commit()
    return "Success"

    conn.close()
    return jsonify(api_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
