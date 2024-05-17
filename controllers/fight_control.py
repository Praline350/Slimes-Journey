import os
import sys
import time
from tinydb import TinyDB, Query
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, PassiveEvent, ActiveEvent
from models.trailer import Trailer 


class FightController:
    def __init__(self):
        
