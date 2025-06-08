from effect import *
from dice import *
from item import *
from character import Character
from mob import Mob

class Player(Character):
    def __init__(self, name, hp, weapon: Weapon, passive: Passive, active_slots = 3):
        super().__init__(name, hp)
        self.weapon = weapon
        self.passive = passive
        self.active_items: list[Active] = []
        self.active_slots = active_slots
        self.turn_action = 3
        self.log: list[str] = []

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

    def take_turn(self, opponents: list[Mob]):
        self.display_battle_status(opponents)
        cmd = input(f"{self.name} (HP:{self.hp}, Actions:{self.turn_action}) >> ").strip().split()
        if not cmd:
            return

        action = cmd[0].lower()

        if action == "attack" and len(cmd) == 2:
            try:
                idx = int(cmd[1]) - 1
                target = opponents[idx]
                if not target.is_alive():
                    print("YOU ALREADY KILLED THAT GUY.")
                    return
                
                damage = self.weapon.damage
                roll = roll_d20()
                result = interpret_roll(roll)
                if result == "Fumble":
                    damage = 0
                if result == "Failure":
                    damage = 1
                if result == "Success":
                    damage = self.weapon.damage
                if result == "Critical":
                    damage = int(self.weapon.damage * 1.15)
                if result == "Super Critical!":
                    damage = int(self.weapon.damage * 1.5)

                # will add effect +damage

                target.take_damage(damage)
                print(f"You Rolled {roll}({result}) and dealt {damage} to {target.name}!")
                print(f"{target.name}'s HP: {target.hp}")
                self.log.append(f"{self.name} attacked {target.name}: {roll}({result}) -> {damage}")
                self.turn_action -= 1
            except (ValueError, IndexError):
                print("Usage: attack <vaild_enemy_index>")

        elif action == "inventory":
            print(f"Weapon: {self.weapon.name} (Damage: {self.weapon.damage})")
            print(f"Passive: {self.passive.name if self.passive else 'None'}")
            print("Active Items:")
            if not self.active_items:
                print(" (None)")
            else:
                for i, it in enumerate(self.active_items, start=1):
                    print(f"  [{i}] {it.name} (Uses left: {it.uses})")


        elif action == "use" and len(cmd) in (2,3):
            try:
                slot = int(cmd[1]) - 1
                item = self.active_items[slot]
                if len(cmd) == 3:
                    tidx = int (cmd[2]) - 1
                    target = opponents[tidx]
                else:
                    target = self

                roll, result, value = item.use(self, target)
                    
                print(
                    f"You used {item.name} on "
                    f"{'self' if target is self else target.name}. "
                    f"{roll}({result}) -> {value}"
                )
                self.log.append(
                    f"{self.name} used {item.name} on "
                    f"{'self' if target is self else target.name}: "
                    f"{roll}({result}) → {value}"
                )

                if item.uses <= 0:
                    self.active_items.pop(slot)
                self.turn_action -= 1
            except (ValueError, IndexError):
                print("Usage: use <valid_item_index> [<enemy_index>]")

        elif action == "save":
            self.save_system.save_player(self, self.player_log)
            print("Game saved.")

        elif action == "quit":
            print("Exiting game.")
            exit(0)

    def attack(self, target: Mob):
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
    
    def display_battle_status(self, opponents: list[Mob]):
        print("========= Current Situation =========")
        names = ["YOU"] + [m.name for m in opponents]
        hps = [f"HP:{self.hp}"] + [f"HP:{m.hp}" for m in opponents]
        widths = [max(len(n), len(h)) for n, h in zip(names, hps)]
        for name, w in zip(names, widths):
            print(name.ljust(w + 2), end='')
        print()
        for hp, w in zip(hps, widths):
            print(hp.ljust(w + 2), end='')
        print()
        total_width = sum(widths) + 2 * len(widths)
        print("=" * total_width)
