import os
import time
import threading
from tinydb import TinyDB, Query

PNJ_DATA_PATH = "../data/"
ENEMY_DATA_PATH = "../data/pnj/pnj_enemy_data.json"

class Enemy:
    def __init__(self):
        self.db_enemy = TinyDB(ENEMY_DATA_PATH, indent=4, encoding="utf-8")


    def write_init(self, name, race, level, hp, attack, defense):
        data = {
            'name': name,
            'race': race,
            'level': level,
            'hp': hp,
            'attack': attack,
            'defense': defense,
            'skills': []
        }
        self.db_enemy.insert(data)

