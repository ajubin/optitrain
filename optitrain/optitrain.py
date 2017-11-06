'''
http://flask.pocoo.org/docs/0.12/tutorial/dbcon/#tutorial-dbcon
'''

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'optitrain.db'),
    SECRET_KEY='dev key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('OPTITRAIN_SETTINGS', silent = True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    '''opens a new database connection if there is non yet'''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    init_db()
    print("Initialized the database")

@app.route("/")
def show_trips():
    db = get_db()
    cur = db.execute('SELECT email, origin, dest, trip_date FROM trip ORDER BY id desc')
    entries = cur.fetchall()
    return render_template('show_trips.html', entries=entries)

@app.route("/add", methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO trip (email, origin, dest, trip_date) VALUES' \
    '(?,?,?,?)', [request.form['email'], request.form['origin'], request.form['dest'], request.form['trip_date']])
    db.commit()
    flash('New trip was successfuly added')
    return redirect(url_for('show_trips'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_trips'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_trips'))
