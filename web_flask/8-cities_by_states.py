#!/usr/bin/python3
"""
Start a Flask application
"""
from flask import Flask, render_template
from models import storage
from models import *
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exc):
    """close the current session"""
    storage.close()


@app.route('/cities_by_states')
def cities_list():
    """returns a list of all state objects"""
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
