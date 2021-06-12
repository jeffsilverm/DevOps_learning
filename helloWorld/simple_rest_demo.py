#! /usr/bin/env python3
#
# A simple flask demo implementing a simple JSON REST interface
# From https://python.plainenglish.io/create-a-simple-rest-api-using-python-flask-framework-1d8b491af648
from flask import Flask
from flask import json
from flask import request


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getjson')
def getjson():
    return json.dumps({"name":"king","likes":"batman"})

@app.route('/save-get')
def saveget():
    if request.method=='GET':
       a=request.args.get('name', '')
       b=request.args.get('email', '')
       return "Name : "+a+" ,  Email :  "+b
    else:
        return "Not get method"


@app.route('/save-post',methods=['POST'])
def savepost():
    if request.method=='POST':
       a=request.form['name']
       b=request.form['email']
       return "Name :  "+a+"  Email:  "+b
    else:
        return "error"

if __name__ == "__main__":
    #app.run()
    app.run(debug=True)