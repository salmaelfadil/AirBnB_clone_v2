#!/usr/bin/python3
"""
python flask script
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)
storage.all()


@app.teardown_appcontext
def teardown_data(self):
    """
    close storage
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filter(id=None):
    """routing to hbnb filters"""
    data = storage.all(State)
    states = []
    for i in data:
        states.append(data[i])
    data = storage.all(Amenity)
    amenities = []
    for k in data:
        amenities.append(data[k])
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)