from player import Player
from item import Weapon, Passive, Active
from monster import Mob, EliteMob
from battle import monster_turn
from save_load import save_game, load_game 

# 아이템 사전 정의
item_dict = {
    "Iron Sword": Weapon("Iron Sword", damage=10, effect={"type": "heal", "value": 5}),
    "Shield": Passive("Shield", effect={"type": "defense_boost", "value": 3}),
    "Healing Potion": Active("Healing Potion", effect={"type": "heal", "value": 30}),
}

# 로드 여부 선택
load = input("Load previous game? (y/n): ").lower()
if load == 'y':
    player, monsters = load_game(item_dict)
else:
    # 초기화
    player = Player("Hero")
    player.equip_item(item_dict["Iron Sword"])
    player.equip_item(item_dict["Shield"])
    player.equip_item(item_dict["Healing Potion"])

    # 몬스터 생성
    mob1 = Mob("Goblin", 60, 10, 5, ["Gold"])
    mob2 = Mob("Orc", 80, 30, 3, ["Gem"])
    mob3 = Mob("Troll", 100, 60, 10, ["Club"])
    elite = EliteMob("Dragon", 150, 50, 15, ["Dragon Scale"], "Fire Breath", 70)
    monsters = [mob1, mob2, mob3, elite]

# 전투 시작
while player.hp > 0 and any(monster.is_alive() for monster in monsters):
    for monster in monsters:
        if monster.is_alive():
            player.attack(monster)
            if not monster.is_alive():
                print(f"{monster.name} has been defeated!")
    monster_turn(monsters, player)

# 결과 출력
if player.hp > 0:
    print("You Win!")
else:
    print("You Died...")

# 저장 여부 선택
save = input("Save current progress? (y/n): ").lower()
if save == 'y':
    save_game(player, monsters)
