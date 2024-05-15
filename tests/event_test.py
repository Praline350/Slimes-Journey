import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent


event = PassiveEvent()
data = event.spwan_event()
data = event.get_event_data(data['name'])
print(data)





