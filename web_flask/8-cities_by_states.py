#!/usr/bin/python3
"""
This script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all State objects in DBStorage"""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(arg=None):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
