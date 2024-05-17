import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tinydb import TinyDB, Query
from models.character import Character, ActionPlayer
from models.pnj import Enemy


character = Character()
action = ActionPlayer()

def reorder_entry(entry):
    ordered_entry = {
        "id": entry.get("id"),
        "viewer": entry.get("viewer"),
        "online": entry.get("online"),
        "name": entry.get("name"),
        "level": entry.get("level"),
        "hp": entry.get("hp"),
        "attack": entry.get("attack"),
        "defense": entry.get("defense"),
        "intel": entry.get("intel"),
        "social": entry.get("social"),
        "style": entry.get("style")
    }
    return ordered_entry

def test1():
    character.add_field_to_all('viewer', "")
    all_chara = character.table_character.all()
    reorder = [reorder_entry(chara) for chara in all_chara]
    character.table_character.truncate()
    for chara in reorder:
        character.table_character.insert(chara)

def test_inscription():
    character.write_new_character("Popole")


def write_vote():
    action.remove_vote()
    print('ok2')
    
def incr_vote():
    player_name = 'dakimedoko'
    user_choice = 2
    action.incr_user_choice(user_choice, player_name)

def all_vote():
    votes = action.db_vote.all()
    vote_max = None
    max_count = 0
    for vote in votes:
        count = vote.get('count')
        if count > max_count:
            max_count = count
            vote_max = vote
    return vote_max
    

def update_character():
    player_name = 'lordlama92'
    key = "hp"
    amount = 3
    character.update_stat(player_name, key, amount)

def voting():
    vote = all_vote()
    print(vote['player_id_list'])



