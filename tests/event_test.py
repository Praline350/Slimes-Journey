import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent


event = Event()
passive_event = PassiveEvent()
active_event = ActiveEvent()


def event_data():
    event_id = active_event.get_activate_id()
    event = active_event.get_event(event_id)
    choice = event['choices']
    
    i = 0
    general = event['choices'][i]['general']
    print(event['description'])


#event_data()

event_data()

"""while True:
    state = active_event.get_activate_event()
    print(state)
    time.sleep(1)
    if state['state'] == 1:
        break"""






