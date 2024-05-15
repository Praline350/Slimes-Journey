import os
import sys
import threading
from flask import Flask, jsonify
from tinydb import TinyDB, Query 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent
from models.trailer import Trailer



trailer = Trailer()
passive_event = PassiveEvent()
event = Event()

    



def play():
    current_position = trailer.table_trailer.get(Query().name == 'Trailer')['position']
    while current_position < 5:

        data = passive_event.spwan_event()
        passive_event.get_event_data(data['name'])
        trailer.update_inventory(data['key'], data['amount'])
        event.write_current_event(data)
        current_position = trailer.move_trailer()
    current_position = 0
    trailer.table_trailer.update({'position': current_position}, Query().name == 'Trailer')


if __name__ == "__main__":
    play() 