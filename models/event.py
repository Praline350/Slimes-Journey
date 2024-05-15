import os
import time
from tinydb import TinyDB, Query
import random
from flask import Flask, jsonify

EVENT_DATA_PATH = "../data/event_data.json"

class Event:
    def __init__(self):
        self.db_event = TinyDB(EVENT_DATA_PATH, indent=4, encoding='utf-8')
        self.table_current_event = self.db_event.table('Current_event')
    
    def write_init(self):
        data = {
            'name': '',
            'desc': '',
            'key': '',
            'amount': ''
        }
        self.table_current_event.insert(data)
        
    def write_current_event(self, data):
        self.table_current_event.update(data, doc_ids=[1])




class PassiveEvent(Event):
    def __init__(self):
        super().__init__()
        self.passive_table = self.db_event.table('Passive')
        
    
    def write_p_event(self, name, desc, key, amount):
        data = {
            'name': name,
            'desc': desc,
            'key': key,
            'amount': amount
        }
        self.passive_table.insert(data)

    def spwan_event(self):
        all_passive_events = self.passive_table.all()
        random_event = random.choice(all_passive_events)
        return random_event
    
    
    def get_event_data(self, name):
        data = self.passive_table.get(Query().name == name)
        return data


class ActiveEvent(Event):
    def __init__(self):
        super().__init__()
        self.active_table = self.db_event.table('Active')



