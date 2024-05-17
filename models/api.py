import os
import sys
from flask import Flask, jsonify
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent
from models.trailer import Trailer

app = Flask(__name__)
event = Event()
trailer = Trailer()
p_event = PassiveEvent()
a_event = ActiveEvent()



@app.route('/passive-event', methods=['GET'])
def get_current_p_event():
    """
    Route API pour les events, récupère le current_event => l'envoie sur l'API
    """
    event_data = p_event.db_p_event.all()
    response = jsonify(event_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/active-event', methods=['GET'])
def get_current_a_event():
    """
    Route API pour les events, récupère le current_event => l'envoie sur l'API
    """
    event_data = a_event.db_a_event.all()
    response = jsonify(event_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trailer-inventory', methods=['GET'])
def get_trailer_inventory():
    inventory_data = trailer.table_trailer_inventory.get(doc_id=1)
    response = jsonify(inventory_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run(debug=True)
