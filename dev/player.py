from effect import *
from dice import *
from item import *
from character import Character

class Player(Character):
    def __init__(self, name, hp, weapon: Weapon, passive: Passive, active_slots = 3):
        super().__init__(name, hp)
        self.weapon = weapon
        self.passive = passive
        self.active_items: list[Active] = []
        self.active_slots = active_slots
        self.turn_action = 3

    def reset_action(self):
        self.turn_action = 3

    def defend(self, damaged):
        buff = 0
        if isinstance(self.passive.effect, DefenseReductionEffect):
            buff = self.passive.effect.apply(0, "")
        damaged = max(0, damaged - buff)
        roll = roll_d20()
        result = interpret_roll(roll)

        if result not in ("Fumble!", "Failure") and self.passive.DefenseReductionEffect:
            damaged = self.passive.DefenseReductionEffect.apply(damaged, result)
        elif result == "Fumble!":
            print(f"Defense Roll - Fumbled! | You take full damage!")
        self.hp = max(0, self.hp - damaged)
        
        return damaged

    def take_turn(self, opponents):
        self.apply_statuses()
        pass

    def attack(self, target: Character):
        roll = roll_d20()
        result = interpret_roll(roll)
        buff = 0
        if isinstance(self.weapon.effect, DamageBonusEffect):
            buff = self.weapon.effect.apply(0, "")
        damage = self.weapon.damage + buff  
        print(f"{self.name} Rolled the Dice : {roll} ({result})")

        if result == "Fumble!":
            print("You Missed Attack!")
            damage = 0
        if result == "Failure":
            damage = 5
        elif result == "Success":
            pass
        elif result == "Critical":
            damage = (damage * 1.2)
        elif result == "Super Critical!":
            damage = (damage * 1.5)

        target.take_damage(damage)
        print(f"You Damaged {damage} to {target.name}!")

    def use_active(self, slot_idx, target: Character):          # will be detatiled later
        if slot_idx < 0 or slot_idx >= len(self.active_items):
            raise IndexError("Invalid active slot")
        item = self.active_items[slot_idx]
        roll = roll_d20()
        result = interpret_roll(roll)
        val = 0
        if result not in ("Fumble!", "Failure") and item.effect:
            val = item.effect.apply(roll, result)
        if item.status:
            if result in ("Success", "Critical", "Super Critical!"):
                dur = item.status.duration + (1 if result == "Super Critical!" else 0)
                target.add_status(type(item.status)(**{k:v for k, v in item.status.__dict__.items() if k!='duration'}, duration = dur))
            elif result == "Fumble!":
                self.add_status(type(item.status)(**{k:v for k, v in item.status.__dict__.items() if k!='duration'}, duration = item.status.duration))
        item.uses -= 1
        if not item.targets:
            self.heal(val)
        else:
            target.take_damage(val)
        
        if item.uses <= 0:
            self.active_items.pop(slot_idx)
        self.turn_action -= 1
        return roll, result, val
