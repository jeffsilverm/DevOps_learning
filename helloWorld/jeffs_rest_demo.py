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
# From https://python.plainenglish.io/create-a-simple-rest-api-using-python
# -flask-framework-1d8b491af648    # noqa


import json
from os import path

from flask import Flask
from flask import json
from flask import request
from werkzeug import datastructures
from werkzeug.exceptions import MethodNotAllowed, Conflict, NotFound

from tests.test_get import DATABASE_FILENAME


class ApiV1(object):
    """This class implements version 1 of the API.  Implementing the API
    this way is suggested by the book
    Undisturbed REST: a guide to designing the perfect API
    by Michael Stowe"""

    def __init__(self):
        if not path.exists(DATABASE_FILENAME):
            # If the database file does not exist, then create it.
            self.database = {"jeff": "jeffsilverm@gmail.com",
                             "jeffs": "jeffsilverman.924@gmail.com"}
            self.save_database()
        else:
            self.load_database()

    def load_database(self) -> None:
        with open(DATABASE_FILENAME, "r") as dbf:
            self.database = json.load(dbf)

    def save_database(self) -> None:
        with open(DATABASE_FILENAME, "w") as dbf:
            json.dump(obj=self.database, fp=dbf)

    def get(self, name: str) -> str:
        print(
            f"in get(): name={name} value="
            f"{self.database.get(name, 'NOT FOUND!')}, "
            f"{name in self.database}")
        if name not in self.database:
            print(f"What's in the database? {self.database}")
            raise NotFound
        return self.database[name]

    def post(self, name: str, email: str) -> None:
        if name in self.database:
            raise Conflict
        self.database[name] = email
        self.save_database()

    def put(self, name: str, email: str) -> None:
        self.database[name] = email
        self.save_database()

    def delete(self, name: str) -> None:
        if name in self.database:
            del self.database[name]


app = Flask(__name__)

api = ApiV1()


# By default, if no methods are specified, then GET and HEAD are accepted and
# nothing else
@app.route("/v1/")
def v1_api_get0():
    # Come here if the URL is of the form /v1/?name=jeffs
    # request is an instance of flask.Request, see
    # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request
    args: datastructures.ImmutableMultiDict = request.args
    print(f"in v1_api_get0: args is {args}")
    name = args['name']
    return v1_api_get1(name)


@app.route("/v1/<name>")
def v1_api_get1(name):
    """This method handles API version 1 calls"""
    if len(api.database) == 0:
        api.load_database()
    assert isinstance(api.database, dict), "api.database should be a dict, " \
                                           f"but it's actually a " \
                                           f"{type(api.database)}"
    print(f"GET method: name={name} value={api.database.get(name, 'NOT FOUND!')}")
    # Converting result to a JSON style string is a stopgap measure.  This
    # should be type sensitive
    result = {name: api.get(name)}
    return result


@app.route("/v1/", methods=['POST', 'PUT', 'DELETE'])
def v1_apt_not_get():
    name = request.form['name']
    args: datastructures.ImmutableMultiDict = request.args
    print(f"method is {request.method}. name={name} and type={type(name)}")
    if request.method == 'POST':
        result = api.post(name=name,
                          addr=args.get('email', default=None, type=None))
    elif request.method == 'PUT':
        result = api.post(name=name,
                          addr=args.get('email', default=None, type=None))
    elif request.method == 'DELETE':
        result = api.delete(name=name)
    else:  # Not sure how this can happen
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
