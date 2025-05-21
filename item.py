class Item:
    def __init__(self, name, effect=None):
        self.name = name
        self.effect = effect

class Weapon(Item):
    def __init__(self, name, damage, effect=None):
        super().__init__(name, effect)
        self.damage = damage

class Passive(Item):
    pass

class Active(Item):
    def use(self, player):
        if self.effect:
            player.apply_effect(self.effect)
            return True
        return False
