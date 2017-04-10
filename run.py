import sys
import os
from jinja2 import evalcontextfilter, Markup, escape
from flask import Flask, render_template, request, escape, \
        send_from_directory, g, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(12)

class User():
    def __init__(self, id, name, username, password, location, phone):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.location = location
        self.phone = phone

default = User(0, "user", "user", "password", "null", "0400000000")
richard = User(1, "richard", "richard", "sausage", "UNSW", "93856666")
USERS = [default, richard]

@app.route('/', methods=['GET', 'POST'])
def index():

    if "username" in session and not find(session["username"]):
            session.pop('username', None)
            return redirect(url_for('index'))

    if "username" in session:
        if request.method == "POST":
            user_input = request.form['query'].strip()
            user = find(session["username"])
            return render_template('home.html',
                    user = user, user_input = user_input, string = user_input.format(user), version = sys.version)

        else:
            user = find(session["username"])
            return render_template('home.html', user = user, version = sys.version)
    else:
        error = ''
        return render_template('base.html', error = error, version = sys.version)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = request.args.get("error", "")
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if valid(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', error = "incorrect credentials"))
    else:
        return render_template('login.html', error = error, version = sys.version)


@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/debug')
def debug():
    return "We gotta be sneaky. we gotta be sneaky Charlie, ssneakyyy"

def find(username):
    for user in USERS:
        if user.username == username:
            return user
    return False

def valid(username, password):
    for user in USERS:
        if user.username == username and user.password == password:
            return True
    return False


if __name__ == '__main__':
    # you should be using this to debug. This allows you to attach an actual debugger to
    # your script, and you can see any errors that occurred in the command line. No pesky
    # log files like cgi does Also note that since use_reloader is on, you shouldn't make
    # changes to the code while the app is paused in a debugger, because it will reload as
    # soon as you hit play again
    app.run(debug=True, use_reloader=True, port=5555)

