import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.item import Item

item = Item()
item.write_item('Burger', 'Consumable')