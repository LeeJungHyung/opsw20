from character import Character
from drop_table import *
from dice import *
from player import Player


class Mob(Character):           # type : 'normal', 'elite', 'boss'
    def __init__(self, name, hp, attack, skill = None, skill_chance: float = 0.0, mob_type = 'normal'):
        super().__init__(name, hp)
        self.atk = attack
        self.skill = skill
        self.skill_chance = skill_chance
        self.mob_type = mob_type

    def get_drops(self, max_drops = 1):
        return roll_drops(self.mob_type, max_drops)

    def take_turn(self, opponents):
        self.apply_statuses()
        roll = roll_d20()
        result = interpret_roll(roll)
        damage = self.atk if result not in ("Fumble", "Failure") else 0
        
        if self.skill and random.random() < self.skill_chance:
            damage += self.skill.apply(roll, result)
        target = opponents[0]
        
        if isinstance(target, Player):
            damage = target.defend(damage)
        
        else:
            target.take_damage(damage)
        
        return roll, result, damage
