#!/usr/bin/python3
"""Starts a flask web application"""

from flask import Flask, render_template

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


@app.route("/python/<text>")
def python_is_cool(text='is cool'):
    """Prints a statement on webpage"""
    return "Python {}".format(text.replace('_', ' '))


@app.route("/number/<int:n>")
def number_n(n):
    """Prints a statement on webpage"""
    return "{:d} is a number".format(n)


@app.route("/number_template/<int:n>")
def number_template(n):
    """Prints a statement on webpage"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def odd_even_template(n):
    """Prints a statement on webpage"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
