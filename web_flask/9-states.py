#!/usr/bin/python3
"""
This script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays an HTML page with a list of all State objects in DBStorage"""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown_db(arg=None):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
