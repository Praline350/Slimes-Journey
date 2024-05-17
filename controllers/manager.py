import os
import sys
import time
from tinydb import TinyDB, Query
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent
from models.trailer import Trailer 



class Manager:
    def __init__(self):
        self.trailer = Trailer()
        self.passive_event = PassiveEvent()
        self.active_event = ActiveEvent()
        self.event = Event()
        
    

    def gameplay_loop_passive(self):
        while self.trailer.timer is False:
            print('départ')
            self.trailer.progress()
            print('timer')
            self.trailer.move_trailer()
            self.run_passive_event()
            self.trailer.timer = False
            time.sleep(1)

    def gameplay_loop_active(self):
        while self.trailer.timer is False:
            print('départ')
            self.trailer.progress()
            print('timer')
            self.trailer.move_trailer()
            self.run_active_event()
            self.trailer.timer = False
            time.sleep(1)

    def run_passive_event(self):
        data_event = self.event.spawn_event('passive')
        self.trailer.update_inventory(data_event['key'], data_event['amount'])


    def run_active_event(self):
        current_event = self.active_event.spawn_event()
        self.active_event.toggle_state_true()
        event_id = self.active_event.get_activate_id()
        while current_event['state'] != 1:
            current_event = self.active_event.get_event(event_id)
            print(current_event['state'])
            print('attente commande')
            time.sleep(2)
        self.choice_user_event()
        self.active_event.toggle_state_false()
        self.active_event.deactivate_event()
        
    def choice_user_event(self):
        self.active_event.progress()
        event_id = self.active_event.get_activate_id()
        while self.active_event.timer is False:
            print('Donnez votre choix !')
            time.sleep(2)
        self.active_event.timer = False
        choice = self.active_event.result_user_choice(event_id)
        print(choice)
            
            

manager = Manager()
manager.gameplay_loop_active()



