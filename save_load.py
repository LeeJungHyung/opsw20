import json
from monster import Mob, EliteMob
from player import Player

def save_game(player, monsters, filename='save.json'):
    data = {
        'player': {
            'name': player.name,
            'hp': player.hp,
            'attack': player.attack,
            'defense': player.defense,
            'items': [item.name for item in player.items]  
        },
        'monsters': []
    }

    for m in monsters:
        monster_data = {
            'type': 'EliteMob' if isinstance(m, EliteMob) else 'Mob',
            'name': m.name,
            'hp': m.hp,
            'attack': m.attack,
            'defense': m.defense,
            'drops': m.drops,
        }
        if isinstance(m, EliteMob):
            monster_data['skill_name'] = m.skill_name
            monster_data['skill_power'] = m.skill_power
        data['monsters'].append(monster_data)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print("Game saved!")

def load_game(item_dict, filename='save.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    p_data = data['player']
    player = Player(p_data['name'])
    player.hp = p_data['hp']
    player.attack = p_data['attack']
    player.defense = p_data['defense']

    for item_name in p_data['items']:
        if item_name in item_dict:
            player.equip_item(item_dict[item_name])
        else:
            print(f"Warning: Item '{item_name}' not found.")

    monsters = []
    for m in data['monsters']:
        if m['type'] == 'EliteMob':
            monster = EliteMob(
                m['name'], m['hp'], m['attack'], m['defense'],
                m['drops'], m['skill_name'], m['skill_power']
            )
        else:
            monster = Mob(
                m['name'], m['hp'], m['attack'], m['defense'],
                m['drops']
            )
        monsters.append(monster)

    print("Game loaded!")
    return player, monsters
