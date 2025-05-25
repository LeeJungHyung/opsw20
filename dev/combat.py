import random
from dice import *
from mob import *
from item import *

class Combat:
    def __init__(self, player, stage = 1):
        self.player player
        self.stage = stage
        self.battle_count = 0
        self.elite_battles = 0

    def start_battle(self):
        print(f"\n")
