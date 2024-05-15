import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.character import Character

character = Character()
character.write_new_character()