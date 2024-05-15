import os
from tinydb import TinyDB, Query

ITEM_DATA_PATH = "../data/item_data.json"
ITEM_CATEGORIES = ["Ressources", "Weapon", "Armor", "Consumable"]


class Item:
    def __init__(self):
        self.db_item = TinyDB(ITEM_DATA_PATH, indent=4, encoding="utf-8")
        self.consumable_item = self.db_item.table("Consumable")
        self.ressource_item = self.db_item.table("Ressources")
        self.weapon_item = self.db_item.table("Weapons")
        self.armor_item = self.db_item.table("Armors")

    def write_ressource_item(self, name):
        data = {"name": name}
        self.ressource_item(data)

    def write_weapon_item(self, name, attack):
        data = {
            "name": name,
            "attack": int(attack),
        }
        self.weapon_item.insert(data)

    def write_armor_item(self, name, defense):
        data = {"name": name, "defense": int(defense)}
        self.armor_item.insert(data)

    def write_consumable_item(self, name):
        data = {"name": name}
        self.consumable_item.insert(data)
