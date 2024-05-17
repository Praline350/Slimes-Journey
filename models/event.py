import os
import time
import threading
from tinydb import TinyDB, Query
import random
from flask import Flask, jsonify

EVENT_DATA_PATH = "../data/event/event_data.json"
CURRENT_DATA_PATH = "../data/event/current_event_data.json"
P_EVENT_DATA_PATH = "../data/event/passif_event_data.json"
A_EVENT_DATA_PATH = "../data/event/actif_event_data.json"

VOTE_DATA_PATH = "../data/action/vote_data.json"

class Event:
    def __init__(self):
        self.db_current_event = TinyDB(CURRENT_DATA_PATH, indent=4, encoding='utf-8')
        self.db_passive_event = TinyDB(P_EVENT_DATA_PATH, indent=4, encoding='utf-8')
        self.db_active_event = TinyDB(A_EVENT_DATA_PATH, indent=4, encoding='utf-8')
    
    def make_id(self, type_event):
        if type_event == 'active':
            self.db = self.db_active_event
        if type_event == 'passive':
            self.db = self.db_passive_event

        all_event = self.db.all()
        if all_event:
            last_id = max(event.doc_id for event in all_event)
        else:
            last_id = 0
        new_id = last_id + 1
        return new_id

    def update_event(self, id_event):
        pass

    def deactivate_event(self, event_type, event):
        self.db = self.get_event_type(event_type)
        EventQuery = Query()
        self.db.update({'activate': False}, EventQuery.id == event['id'])

    def get_event_type(self, event_type):
        if event_type == 'active':
            self.db = self.db_active_event
        if event_type == 'passive':
            self.db = self.db_passive_event
        return self.db




class PassiveEvent(Event):
    def __init__(self):
        super().__init__()
        self.table_current_event = self.db_current_event.table('Passive')
        
    def write_passive_event(self, name, desc, key, amount, drop):
        id = self.make_id('passive')
        data = {
            'id': id,
            'active': False,
            'name': name,
            'desc': desc,
            'drop': drop,
            'key': key,
            'amount': amount
        }
        self.db_passive_event.insert(data)

    def get_event_data(self, name):
        data = self.db_passive_event.get(Query().name == name)
        return data

    def write_current_event(self, data):
        self.table_current_event.update(data, doc_ids=[1])


class ActiveEvent(Event):
    def __init__(self):
        super().__init__()
        self.db_vote = TinyDB(VOTE_DATA_PATH, indent=4, encoding='utf-8', ensure_ascii=False)
        self.table_current_event = self.db_current_event.table('Active')
        self.timer = False

    def get_activate_id(self):
        """Return : activate event ID"""
        EventQuery = Query()
        result = self.db_active_event.search(EventQuery.activate == True)
        if result:
            return result[0]['id']
        return None

    def get_event(self, event_id):
        """Return : Event data dict json  """
        current_event = self.db_active_event.get(doc_id=event_id)
        return current_event

    def spawn_event(self):
        all_events = self.db_active_event.all()
        weighted_events = [(event, event['drop']) for event in all_events]
        events, weights = zip(*weighted_events)
        random_event = random.choices(events, weights=weights, k=1)[0]
        event_id = random_event['id']
        self.activate_event(event_id)
        return random_event
    
    def activate_event(self, event_id):
        EventQuery = Query()
        self.db_active_event.update({'activate': True}, EventQuery.id == event_id)

    def deactivate_event(self):
        event_id = self.get_activate_id()
        current_event = self.get_event(event_id)
        current_event['activate'] = False
        self.db_active_event.update({'activate': current_event['activate']}, doc_ids=[event_id])

    def write_current_event(self, data):
        self.table_current_event.update(data, doc_ids=[1])
        current_data = self.table_current_event.get(doc_id=1)
        print(current_data)
        return current_data

    def get_state_event(self):
        event_id = self.get_activate_id()
        event = self.get_event(event_id)
        if event:
            state = event['state']
            return state
        return None

    def toggle_state_true(self):
        event_id = self.get_activate_id()
        event = self.get_event(event_id)
        if event:
            self.db_active_event.update({'state': event['state'] + 1}, doc_ids=[event_id])
            return event
        return None

    def toggle_state_false(self):
        event_id = self.get_activate_id()
        event = self.get_event(event_id)
        if event:
            self.db_active_event.update({'state': event['state'] - 2}, doc_ids=[event_id])
        return None
    
    def activate_vote(self):
        event_id = self.get_activate_id()
        event = self.get_event(event_id)
        choices = event['choices']
        for i in range(len(choices)):
            print(i)
            general = event['choices'][i]['general']
            personal = event['choices'][i]['personal']
            id = i +1
            self.db_vote.update({'general': general}, doc_ids=[id])
            self.db_vote.update({'personal': personal}, doc_ids=[id])
    
    def all_event_off(self):
        all_events = self.db_active_event.all()
        for event in all_events:
            event_id = event['id']
            event['activate'] = False
            event['state'] = -1
            event['user_choices'][0] = {'1':0, '2':0}
            self.db_active_event.update({'activate': event['activate']}, doc_ids=[event_id])
            self.db_active_event.update({'state': event['state']}, doc_ids=[event_id])
            self.db_active_event.update({'user_choices': event['user_choices']}, doc_ids=[event_id])
        
        

    

    def progress(self):
        threading.Thread(target=self.start_timer).start()

    def start_timer(self):
        time.sleep(10)
        self.timer = True
        return self.timer



