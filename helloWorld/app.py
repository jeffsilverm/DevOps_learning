#! /usr/bin/env python3
from flask import Flask, render_template, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
# curl -i http://localhost:5000
# curl -i http://localhost:5000/

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

with app.test_request_context():
    # print(url_for('index.html')) # This raises an exception, werkzeug
    # .routing.BuildError: Could not build url for endpoint
    # 'index.html'. Did you mean &apos;render_static&apos; instead?
    # I don't know what meant.
    print(url_for('hello'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))



if __name__ == '__main__':
    app.run()