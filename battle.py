def monster_turn(monsters, player):
    for monster in monsters:
        if monster.is_alive():
            monster.attack_target(player)
