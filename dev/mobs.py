import random
from character import Character
from player import Player
from drop_table import roll_drops
from dice import roll_d20, interpret_roll


class Skill:
    def __init__(self, name, description, base_power):
        self.name = name
        self.description = description
        self.base_power = base_power

    def apply(self, roll, result):
        if result == "Super Critical!":
            return int(self.base_power * 2)
        elif result == "Critical":
            return int(self.base_power * 1.5)
        elif result == "Success":
            return self.base_power
        elif result == "Partial":
            return int(self.base_power * 0.5)
        return 0


class Mob(Character):  
    def __init__(self, name, hp, attack, skills, skill_chance: float = 0.3, mob_type='normal'):
        super().__init__(name, hp)
        self.atk = attack
        self.skills = skills 
        self.skill_chance = skill_chance
        self.mob_type = mob_type

    def get_drops(self, max_drops=1):
        return roll_drops(self.mob_type, max_drops)

    def take_turn(self, opponents):
        self.apply_statuses()
        roll = roll_d20()
        result = interpret_roll(roll)

        damage = self.atk if result not in ("Fumble!", "Failure") else 0

       
        if self.skills and random.random() < self.skill_chance:
            chosen_skill = random.choice(self.skills)
            print(f"{self.name} uses skill: {chosen_skill.name}!")
            damage += chosen_skill.apply(roll, result)

        target = opponents[0]
        if isinstance(target, Player):
            damage = target.defend(damage)
        else:
            target.take_damage(damage)

        return roll, result, damage




def Junior_Time_Warden():
    skills = [
        Skill("Temporal Flick", "A quick jab that confuses time perception.", 5),
        Skill("Minor Rewind", "Restores minor HP if hit is successful.", 0),  
        Skill("Stutter Step", "Reduces opponent's initiative.", 4),
        Skill("Time Zap", "Sends a temporal shockwave.", 6),
    ]
    return Mob("Junior_Time_Warden", hp=50, attack=10, skills=skills, skill_chance=0.3, mob_type="normal")


def Senior_Time_Warden():
    skills = [
        Skill("Chronolock", "Locks target in a moment of time.", 10),
        Skill("Phase Distort", "Deals damage and slows target.", 12),
        Skill("Temporal Slash", "Cuts through timelines.", 14),
        Skill("Rewind Burst", "Damages all nearby enemies.", 11),
    ]
    return Mob("Senior_Time_Warden", hp=65, attack=15, skills=skills, skill_chance=0.4, mob_type="elite")


def Devourer_of_Time():
    skills = [
        Skill("Collapse Reforged", "Rewrites current time state with damage.", 18),
        Skill("Chrono Eruption", "Explodes stored time energy.", 20),
        Skill("Void Pulse", "A wave of nothingness saps the will.", 22),
        Skill("Timeless Bite", "A physical slash imbued with temporal energy.", 24),
    ]
    return Mob("Devourer_of_Time", hp=120, attack=20, skills=skills, skill_chance=0.5, mob_type="boss")
