import random
from typing import List
from dev import mob
from mob import Mob
from drop_table import *

def get_drops(mob: Mob, max_drops = 1):
    return roll_drops(mob.mob_type, max_drops)

        
### NORMAL TYPE ###

def Junior_Time_Warden(loop = 1):       # basic example of normal mob
    return Mob(
        name="Junior Time Warden",
        base_hp=50,
        base_atk=10,
        base_def=0,
        mob_type="normal",
        loop=loop
    )

### ELITE TYPE ###

def Senior_Time_Warden(loop = 1):       # basic example of elite mob
    return Mob(
        name="Senior Time Warden",
        base_hp=65,
        base_atk=15,
        base_def=5,
        skill="Chronolock",
        skill_chance=0.25,
        mob_type="elite",
        loop=loop
    )

### BOSS TYPE ###

def Devourer_of_Time(loop = 1):         # basic example of boss mob
    return Mob(
        name="Devourer of Time",
        base_hp=120,
        base_atk=20,
        base_def=10,
        skill="Collapse Reforged",
        skill_chance=0.3,
        mob_type="boss",
        loop=loop
    )


def get_stage_enemies(loop, stage_number, battle_index):
    enemies = []

    if stage_number == 1:
        if battle_index == 0:
            enemies.append(Junior_Time_Warden(loop))
        else:
            count = random.randint(1, 3)
            for _ in range(count):
                enemies.append(Junior_Time_Warden(loop))

    elif stage_number == 2:
        elite_count = random.randint(1, 2)
        normal_count = random.randint(1, 3)
        for _ in range(elite_count):
            enemies.append(Senior_Time_Warden(loop))
        for _ in range(normal_count):
            enemies.append(Junior_Time_Warden(loop))

    elif stage_number == 3:
        enemies.append(Devourer_of_Time(loop))

    else:
        raise ValueError(f"Invalid stage number: {stage_number!r}")

    return enemies
