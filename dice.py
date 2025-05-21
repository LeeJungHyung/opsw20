import random

def roll_d20():
    return random.randint(1, 20)

def interpret_roll(value):
    if value == 1:
        return "Fumble!"
    elif value <= 8:
        return "Failure"
    elif value <= 16:
        return "Success"
    elif value <= 19:
        return "Critical"
    else:
        return "Super Critical!"
