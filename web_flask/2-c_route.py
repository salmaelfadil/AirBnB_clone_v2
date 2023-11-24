#!/usr/bin/python3
"""Starts a flask web application"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def homepage():
    """Prints a statement on webpage"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb_page():
    """Prints a statement on webpage"""
    return "HBNB"


@app.route("/c/<text>")
def c_is_fun(text):
    """Prints a statement on webpage"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)