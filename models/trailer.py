import os
import time
from tinydb import TinyDB, Query
import threading

TRAILER_DATA_PATH = '../data/trailer_data.json'

class Trailer:
    def __init__(self):
        #Base de donnée
        self.db_trailer = TinyDB(TRAILER_DATA_PATH, indent=4, encoding='utf-8')
        self.table_trailer = self.db_trailer.table('Trailer')
        self.table_trailer_inventory = self.db_trailer.table('Inventory')
        self.timer = False

        #Attributs
        self.speed = 1

    def write_trailer_init(self):
        data = {
            'name': 'Trailer',
            'level': 1,
            'state': 100,
            'atq': 1,
            'def': 1,
            'hp': 50,
            "position": 0
        }
        self.table_trailer.insert(data)

    def write_inventory_init(self):
        data = {
            "ressource": 0,
            "heal": 0,
            "food": 0
        }
        self.table_trailer_inventory.insert(data)

    def update_inventory(self, key, amount):
        inventory = self.table_trailer_inventory.all()
        data = inventory[0]
        data[key] += amount
        self.table_trailer_inventory.update(data, doc_ids=[1])
        print('update')

    def move_trailer(self):
        while not self.timer:
            time.sleep(1)
            print('attente')
        current_position = self.table_trailer.get(Query().name == 'Trailer')['position']
        update_position = current_position + 1
        self.table_trailer.update({'position': update_position}, Query().name == 'Trailer')
        print(update_position)
        return update_position

    def progress(self):
        threading.Thread(target=self.start_timer).start()

    def start_timer(self):
        time.sleep(2)
        self.timer = True
        return self.timer



    def simulate_move(self, duration):
        current_position = self.table_trailer.get(Query().name == 'Trailer')['position']
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(1)
            self.move_trailer()
        current_position = 0
        self.table_trailer.update({'position': current_position}, Query().name == 'Trailer')
        



