from dice import roll_d20, interpret_roll

class Item:
    def __init__(self, name, description, rarity = "common", effect = None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.effect = effect

    def use(self, player):
        print(f"You Used {self.name}!")

    def __str__(self):
        effct = f", Effect : {self.effect}" if self.effect else ""      # Ternary Operators
        return f"{self.name} (({self.rarity}) - {self.description}{effct})"

class Weapon(Item):
    def __init__(self, name, description, damage, effect = None, rarity = "common"):
        super().__init__(name, description, rarity, effect)
        self.damage = damage

class Passive(Item):
    def __init__(self, name, description, rarity="common", effect=None):
        super().__init__(name, description, rarity, effect)

    def use(self, player):
        pass        # override later

class Active(Item):
    def __init__(self, name, description, max_uses, rarity = "common", effect = None):
        super().__init__(name, description, rarity, effect)
        self.max_uses = max_uses
        self.remaining = max_uses

    def use(self, player):
        if self.remaining <= 0:
            print(f"You Can't Use {self.name} Anymore!")
            return False

        super().use(self,player)
        print(f"    REMAIN : {self.remaining - 1} out of {self.max_uses}")

        roll = roll_d20()
        result = interpret_roll(roll)
        self.activate_effect(player, result)

        self.remaining -= 1
        if self.remaining <= 0:
            print(f"{self.name} Has Been Used Up.")
            return True
        return False

    def activate_effect(self, player, result):
        pass        # overrid later
