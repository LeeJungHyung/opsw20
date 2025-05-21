from dice import roll_d20, interpret_roll
from item import Weapon, Passive, Active

class Player:
    def __init__(self, name):
        self.name = name
        self.max_hp = 100
        self.hp = self.max_hp
        self.base_attack = 10
        self.base_defense = 0

        self.weapon_slot = None
        self.passive_slot = None
        self.active_slot = None

    def equip_item(self, item):
        if isinstance(item, Weapon):
            print(f"Switch Weapon to {item.name}.")
            self.weapon_slot = item
        elif isinstance(item, Passive):
            print(f"Switch Passive Item to {item.name}")
            self.passive_slot = item
        elif isinstance(item, Active):
            print(f"Switch Active Item to {item.name}")
            self.active_slot = item

    def get_total_attack(self):
        bonus = self.weapon_slot.damage if self.weapon_slot else 0
        return self.base_attack + bonus

    def get_total_defense(self):
        bonus = self.base_defense
        if self.passive_slot and self.passive_slot.effect:
            if self.passive_slot.effect.get("type") == "defense_boost":
                bonus += self.passive_slot.effect.get("value", 0)
        return bonus

    def attack(self, target):
        roll = roll_d20()
        result = interpret_roll(roll)
        total_attack = self.get_total_attack()
        print(f"{self.name} Rolled the Dice : {roll} ({result})")

        if result == "Fumble!":
            print("You Missed Attack!")
            return

        if result == "Failure":
            damage = 1
        elif result == "Success":
            damage = total_attack
        elif result == "Critical":
            damage = int(total_attack * 1.2)
        elif result == "Super Critical!":
            damage = int(total_attack * 1.5)
        else:
            damage = total_attack

        target.take_damage(damage)
        print(f"You Damaged {damage} to {target.name}!")

        if self.weapon_slot and self.weapon_slot.effect:
            self.apply_effect(self.weapon_slot.effect, target)

    def use_active_item(self):
        if self.active_slot:
            consumed = self.active_slot.use(self)
            if consumed:
                print(f"You Used {self.active_slot.name}")
                self.active_slot = None
        else:
            print("You Don't Have Items.")

    def take_damage(self, amount):
        damage = max(0, amount - self.get_total_defense())
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} Damaged {damage}. Remain HP: {self.hp}")

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"{self.name} Healed {amount}. Remain HP: {self.hp}")

    def apply_effect(self, effect, target=None):
        if not effect:
            return

        effect_type = effect.get("type")
        value = effect.get("value", 0)

        if effect_type == "damage_boost":
            print(f"{self.name} gains {value} damage boost effect (not implemented).")
        elif effect_type == "heal":
            self.heal(value)
        elif effect_type == "defense_boost":
            self.base_defense += value
            print(f"{self.name}'s defense increased by {value}!")
        elif effect_type == "critical_rate_up":
            print(f"{self.name} gains critical rate up effect (not implemented).")
        else:
            print(f"Unknown effect type: {effect_type}")
