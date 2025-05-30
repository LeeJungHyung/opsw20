import random
from dev import mob
from mob import *
from drop_table import *

def get_drops(mob: Mob, max_drops = 1):
    return mob.get_drops(max_drops)

def Junior_Time_Warden():       # basic example of normal mob
    return Mob(
        name = "Junior_Time_Warden",
        hp = 50,
        attack = 10,
        mob_type = "normal"
    )

def Senior_Time_Warden():       # basic example of elite mob
    return Mob(
        name = "Senior_Time_Warden", 
        hp = 65, 
        attack = 15, 
        skill = "Chronolock",
        skill_chance = 0.25,
        mob_type = "elite"
    )

def Devourer_of_Time():         # basic example of boss mob
    return Mob(
        name = "Devourer_of_Time", 
        hp = 120, 
        attack = 20,
        skill = "Collapse Reforged",
        skill_chance = 0.3,
        mob_type = "boss"
    )
