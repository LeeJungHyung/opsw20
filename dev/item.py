from effect import *
from dice import roll_d20, interpret_roll

class Item:
    def __init__(self, name, description, rarity = "common", effect: Effect = None, status: StatusEffect = None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.effect = effect
        self.status = status

class Weapon(Item):
    def __init__(self, name, description, damage, rarity = "common", effect: Effect = None, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect, status)
        self.damage = damage

class Passive(Item):
    def __init__(self, name, description, rarity = "common", effect: Effect = None, roll_effect: Effect= None, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect, status)
        self.roll_effect = roll_effect

class Active(Item):     # if target is True -> target of item is Enemy, if False than target is player
    def __init__(self, name, description, rarity = "common", effect: Effect = None, target = False, uses = 1, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect, status)
        self.uses = uses
        self.target = target
