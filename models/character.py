import os
from tinydb import TinyDB, Query

CHARACTER_DATA_PATH = "../data/character_data.json"

class Character:
    def __init__(self):
        self.db_character = TinyDB(CHARACTER_DATA_PATH, indent=4, encoding="utf-8")
        self.table_character = self.db_character.table("Character")

    def write_new_character(self, name):
        if self.table_character.search(Query().name == name):
            return f'{name} Déjà dans le jeu'
        data = {
            'name': name,
            'level': 1,
            'attack': 1,
            'defense': 1,
            'intel': 1,
            'social': 1,
            'style': 1,
        }
        insertion_result = self.table_character.insert(data)
        if insertion_result:
            return f'{name} Bienvenue dans le jeu !'
        else:
            return "Une erreur s'est produite lors de l'inscription."
        

    def get_character_data(self, player_name):
        data = self.table_character.get(Query().name == player_name)
        if data:
            return data
        else:
            return None
