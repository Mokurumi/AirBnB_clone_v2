#!/usr/bin/python3
"""
This script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """
    Displays an HTML page with a list of all States.
    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays an HTML page with about <id>, if it exists."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown_db(arg=None):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
