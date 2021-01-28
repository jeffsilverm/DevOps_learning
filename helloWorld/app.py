#! /usr/bin/env python3
from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run()