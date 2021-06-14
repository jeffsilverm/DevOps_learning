#! /usr/bin/env python3
#
# A not-so-simple flask demo implementing a REST interface
# This is a simple key/value application.  The keys are a name and the value
# is an E-mail address.
#
# Use the following HTTP methods (verbs):
#   GET  to get an E-mail address.  Returns 200 if successful, 404 if address
#        not found, other returns are possible.  This is safe and therefore
#        idempotent.
#   POST to create a new E-mail address.  Returns 200 if successful, 409 if the
#        already exists.  This is not idempotent.
#   PUT will update an existing E-mail address or create a new one if it does
#        not already.  Returns 200 if successful.  This is idempotent.
#   DELETE will delete an existing E-mail address.  If the address does not
#        exist, then that is still successful.  This is idempotent.
#
#
#
# From https://python.plainenglish.io/create-a-simple-rest-api-using-python-flask-framework-1d8b491af648

import sys

from flask import Flask
from flask import json
from flask import request
from werkzeug import datastructures
from werkzeug.exceptions import MethodNotAllowed, Conflict, NotFound
import json
from os import path

DATABASE_FILENAME = "address_list.json"
database = {}

def load_database() -> None:
    global database
    with open(DATABASE_FILENAME, "r") as dbf:
        database = json.load(dbf)


def save_database() -> None:
    global database
    with open(DATABASE_FILENAME, "w") as dbf:
        json.dump(obj=database, fp=dbf)

class ApiV1(object):
    """This class implements version 1 of the API.  Implementing the API
    this way is suggested by the book
    Undisturbed REST: a guide to designing the perfect API
    by Michael Stowe"""

    global database

    def __init__(self):
        load_database()

    def get(self, name: str) -> str:
        print(
            f"in get(): name={name} value={database.get(name, 'NOT FOUND!')}, {name in database}")
        if name not in database:
            print(f"What's in the database? {database}")
            raise NotFound
        return database[name]


    def post(self, name: str, email: str) -> None:
        if name in database:
            raise Conflict
        database[name] = email
        save_database()

    def put(self, name: str, email: str) -> None:
        database[name] = email
        save_database()


    def delete(self, name: str) -> None:
        if name in database:
            del database[name]

if not path.exists(DATABASE_FILENAME):
    # If the database file does not exist, then create it as an empty JSON file
    save_database()

app = Flask(__name__)

api = ApiV1()
@app.route("/v1/", methods=["POST", "PUT", "DELETE"])
@app.route("/v1/<name>", methods=["GET"]  )
def v1_api(name):
    """This method handles API version 1 calls"""
    global database
    if len(database) == 0:
        load_database()
    # request is an instance of flask.Request, see
    # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request
    args: datastructures.ImmutableMultiDict = request.args
    print(f"The method is {request.method}")
    if request.method == 'GET':
        print(f"GET method: name={name} value={database.get(name, 'NOT FOUND!')}")
        result = api.get(name)
    else:
        name = request.form['name']
        print(f"method is {request.method}. name={name} and type={type(name)}")
        if request.method == 'POST':
            result = api.post(name=name, addr=args.get('email', default=None, type=None))
        elif request.method == 'PUT':
            result = api.post(name=name, addr=args.get('email', default=None, type=None))
        elif request.method == 'DELETE':
            result = api.delete(name=name)
        else:   # Not sure how this can happen
            result = None       # Result must be something
            raise MethodNotAllowed
    json_string = json.dumps({"name": name, "email": result}) + "\n"
    return json_string


#
@app.route("/")
def hello():
    return "Hello World!\n"


@app.route('/getjson')
def getjson():
    return json.dumps({"name": "king", "likes": "batman"})


@app.route('/save-get')
def saveget():
    if request.method == 'GET':
        a = request.args.get('name', '')
        b = request.args.get('email', '')
        return "Name : " + a + " ,  Email :  " + b + "\n"
    else:
        return "Not get method"


@app.route('/save-post', methods=['POST'])
def savepost():
    if request.method == 'POST':
        a = request.form['name']
        b = request.form['email']
        return "Name :  " + a + "  Email:  " + b + "\n"
    else:
        return "error"


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
