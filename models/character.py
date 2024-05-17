import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.event import Event, ActiveEvent
from models.trailer import Trailer
from tinydb import TinyDB, Query

CHARACTER_DATA_PATH = "../data/character_data.json"
VOTE_DATA_PATH = "../data/action/vote_data.json"

class Character:
    def __init__(self):
        self.db_character = TinyDB(CHARACTER_DATA_PATH, indent=4, encoding="utf-8")
        self.table_character = self.db_character.table("Character")

    def make_id(self):
        all_event = self.table_character.all()
        if all_event:
            last_id = max(event.doc_id for event in all_event)
        else:
            last_id = 0
        new_id = last_id + 1
        return new_id

    def write_new_character(self, viewer_name):
        if self.table_character.search(Query().viewer == viewer_name):
            return f'{viewer_name} Déjà dans le jeu'
        data = {
            'id': "",
            'viewer': viewer_name,
            'online': False,
            'name': "",
            'level': 1,
            'hp': 100,
            'attack': 1,
            'defense': 1,
            'intel': 1,
            'social': 1,
            'style': 1,
        }
        insertion_result = self.table_character.insert(data)
        if insertion_result:
            return f'{viewer_name} Bienvenue dans le jeu !'
        else:
            return "Une erreur s'est produite lors de l'inscription."
        
    def update_stat(self, viewer_name, key, amount):
        player = self.get_character_data(viewer_name)
        player[key] += amount
        self.table_character.update(player, Query().viewer == viewer_name)


        
    def add_field_to_all(self, field_name, value):
        characters = self.db_character.table('Character')
        all_docs = characters.all()
        
        for doc in all_docs:
            doc_id = doc.doc_id
            # Ajouter le nouveau champ avec la valeur par défaut
            characters.update({field_name: value}, doc_ids=[doc_id])


    def get_character_data(self, viewer_name):
        data = self.table_character.get(Query().viewer == viewer_name)
        if data:
            return data
        else:
            return None
        

    def get_id_player(self, viewer_name):
        PlayerQuery = Query()
        result = self.table_character.search(PlayerQuery.viewer == viewer_name)
        if result:
            player_id = result[0]['id']
            return player_id

class ActionPlayer:
    def __init__(self):
        self.character = Character()
        self.trailer = Trailer()
        self.db_vote = TinyDB(VOTE_DATA_PATH, indent=4, encoding='utf-8')

    def get_player_action(self, player_name):
        self.player_id = self.character.get_id_player(player_name)
        return self.player_id

    def write_init(self):
        for i in range(2):
            data = {
                "choice": i+1,
                "general": "",
                "personal": "",
                "player_list": [],
                "count": 0
            }
            self.db_vote.insert(data)
    
    def remove_vote(self):
        self.db_vote.truncate()
        self.write_init()


    def incr_user_choice(self, user_choice, viewer_name):
        user_choice = int(user_choice)
        vote = self.db_vote.get(doc_id=user_choice)
        new_count = vote.get('count') + 1
        player_list = vote.get('player_list', [])
        player_list.append(viewer_name)
        self.db_vote.update({'count': new_count}, doc_ids=[user_choice])
        self.db_vote.update({'player_list': player_list}, doc_ids=[user_choice])
        


 
    def result_user_choice(self):
        votes = self.db_vote.all()
        vote_max = None
        max_count = 0
        for vote in votes:
            count = vote.get('count')
            if count > max_count:
                max_count = count
                vote_max = vote
        return vote_max
    
    def resolution_event(self, vote_max):
        key = vote_max['general']['key']
        amount = vote_max['general']['amount']
        player_list = vote_max['player_list']
        self.trailer.update_inventory(key, amount)
        for player in player_list:
            key = vote_max['personal']['key']
            amount = vote_max['personal']['amount']
            self.character.update_stat(player, key, amount)
        
        