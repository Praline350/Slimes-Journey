import os
import sys
from flask import Flask, jsonify
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event

app = Flask(__name__)
event = Event()



@app.route('/current_event', methods=['GET'])
def get_current_event():
    """
    Route API pour les events, récupère le current_event => l'envoie sur l'API
    """
    current_event_data = event.table_current_event.all()[0]
    response = jsonify(current_event_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.run(debug=True)
