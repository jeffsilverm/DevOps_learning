#! /usr/bin/env python3
import sys
import pprint

from flask import Flask, render_template, url_for
from markupsafe import escape
from flask import request

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=2 )


@app.route('/login/', methods=['POST', 'GET'])
def login():
    """Flask is going to call login.   """
    request_str = pp.pformat(request)
    print( request_str, file=sys.stderr)
    #if request.method == 'POST':
    #    print("login was called with POST!!!!", file=sys.stderr)
    #    return 'Somehow, /login was called with the POST method\n'
    #else:
    #    print("login was called with GET", file=sys.stderr)
    print (f"The WSGI environment is {request.environ}" )
    print( f"The request.form is {request.form}")
    for k,v in request.form.lists():
        print(k,v)
    username = request.form.get('username')
    password = request.form.get('password')
    app.logger.info(f"{request.environ['REMOTE_ADDR']} , {username}, {password}")
    return f'I got to the end of method login.  username={username} and password={password}\n'

@app.route('/')
def hello():
    return render_template('index.html')
# curl -i http://localhost:5000
# curl -i http://localhost:5000/

# The favorite icon is ignored for now
@app.route('/favicon.ico')
def favicon():
    print("In favicon", file=sys.stderr)
    return "favicon.ico"



if __name__ == '__main__':
# See https://flask.palletsprojects.com/en/2.0.x/debugging/#the-built-in-debugger
# to see what setting debug does.
#    app.run(debug=True)
    app.run(debug=True, use_debugger=False, use_reloader=False)