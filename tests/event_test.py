import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent


event = Event()
passive_event = PassiveEvent()
active_event = ActiveEvent()

"""random_event = event.spawn_event('passive')
print(random_event)"""
active_event.deactivate_event()

"""while True:
    state = active_event.get_activate_event()
    print(state)
    time.sleep(1)
    if state['state'] == 1:
        break"""






