#! /usr/bin/env python3
import sys
import pprint

from flask import Flask, render_template, url_for
from markupsafe import escape
from flask import request

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=2 )

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

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)
# curl -i http://localhost:5000/index/

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s\n' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d\n' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s\n' % escape(subpath)

# See https://flask.palletsprojects.com/en/2.0.x/quickstart/#the-request-object
#with app.test_request_context():
    # print(url_for('index.html')) # This raises an exception, werkzeug
    # .routing.BuildError: Could not build url for endpoint
    # 'index.html'. Did you mean &apos;render_static&apos; instead?
    # I don't know what meant.
#    print(url_for('hello'))
#    print(url_for('login', next='/'))
#    print(url_for('profile', username='John Doe'))

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
    return f'I got to the end of method login.  username={username} and password={password}'

if __name__ == '__main__':
# See https://flask.palletsprojects.com/en/2.0.x/debugging/#the-built-in-debugger
# to see what setting debug does.
#    app.run(debug=True)
    app.run(debug=True, use_debugger=False, use_reloader=False)