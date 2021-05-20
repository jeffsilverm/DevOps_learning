from flask import Flask, render_template, request
# Plagarized from https://overiq.com/flask-101/form-handling-in-flask/
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)

@app.route('/books/<genre>/')
def books(genre):
    return "All Books in {} category".format(genre)


@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('password')
        print( username, password)
        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"

    return render_template('login.html', message=message)

if "__main__" == __name__:
    app.run(debug=True, use_debugger=False, use_reloader=False)