import random
from typing import List
from player import *
from mob import *
from mobs import *
from SaveSystem import SaveSystem

class CombatManager:
    def __init__(self, player: Player, save_system: SaveSystem, player_log: dict):
        self.player = player
        self.save_system = save_system
        self.player_log = player_log
        self.story_shown = False
        self.current_loop = 1
    
    def start_game(self):

        while True:
            print(f"\n ========= Starting Loop {self.current_loop} =========\n")
            for stage in (1, 2, 3):
                if not self.start_stage(stage):
                    return False
            self.current_loop += 1

    def start_stage(self, stage_number: int) -> bool:
        if stage_number == 1:
            return self.stage_one()
        elif stage_number == 2:
            return self.stage_two()
        elif stage_number == 3:
            return self.stage_three()
        else:
            raise ValueError(f"Invalid stage: {stage_number}")

    def stage_one(self) -> bool:
        print(f"--------- Stage 1 (Loop {self.current_loop}) ---------")
        for battle_index in range(5):
            enemies: List[Mob] = get_stage_enemies(self.current_loop, 1, battle_index)
            print(f"\n[Stage 1] Enemies : {[m.name for m in enemies]}")
            survived = self.battle_loop(enemies)
            if not survived:
                return False
            self.post_battle_gap()

        return True

    def stage_two(self) -> bool:
        print(f"--------- Stage 2 (Loop {self.current_loop}) ---------")
        for battle_index in range(4):
            enemies: List[Mob] = get_stage_enemies(self.current_loop, 2, battle_index)
            print(f"\n[Stage 2] Enemies : {[m.name for m in enemies]}")
            survived = self.battle_loop(enemies)
            if not survived:
                return False
            self.post_battle_gap()

        return True

    def stage_three(self) -> bool:
        print(f"--------- Stage 3 (Loop {self.current_loop}) ---------")
        enemies: List[Mob] = get_stage_enemies(self.current_loop, 3, 0)
        print(f"\n[Stage 3] Boss : {[m.name for m in enemies]}")
        survived = self.battle_loop(enemies)
        if not survived:
            return False

        if self.current_loop == 1 and not self.story_shown:
            print("\n YOU DEFEATED THE DEVOURER OF TIME")
            # STROYLINE WILL BE ADDED
            self.story_shown = True

        return True

    def battle_loop(self, enemies: List[Mob]) -> bool:
        self.player.reset_action()
        for mob in enemies:
            mob.reset_turn_state()

        print("\n========= BATTLE START =========")
        print(f"Player: {self.player.name} (HP: {self.player.hp}) VS Enemies: {[m.name for m in enemies]}")
        print("================================\n")

        while self.player.is_alive() and any(m.is_alive() for m in enemies):
            self.player.apply_statuses()
            for mob in enemies:
                mob.apply_statuses()

            self.player.reset_action()
            while self.player.turn_action > 0 and self.player.is_alive():
                self.player.take_turn(enemies)
                if not any(m.is_alive() for m in enemies):
                    break

            if not any(m.is_alive() for m in enemies):
                break

            for mob in enemies:
                if not mob.is_alive():
                    continue
                mob.apply_statuses()

                if mob.is_stunned():
                    self.player_log['battle_logs'].append(f"{m.name} is stunned and skips its turn.")
                    mob.reset_turn_state()
                    continue
                
                if mob.skill and random.random() <= mob.skill_chance:
                    roll, result, damage = mob.use_skill(self.player)
                else:
                    roll, result, damage = mob.attack(self.player)
                
                def_bonus = (self.player.passive.apply_defense_bonus(roll, result) if getattr(self.player, "passive", None) is not None else 0)
                actual = max(0, damage - def_bonus)
                self.player.take_damage(actual)
                
                mob.reset_turn_state()
                if not self.player.is_alive():
                    self.player_log['battle_logs'].append(f"{self.player.name} was defeated by {mob.name}.")
                    break

            if not self.player.is_alive():
                break

        if self.player.is_alive():
            print("\n>>> YOU SURVIVED <<<")
            total_drops = []
            for mob in enemies:
                if not mob.is_alive():
                    total_drops.extend(get_drops(mob, max_drops=1))

            for item in total_drops:
                print(f"Loot dropped: {item.name}")
                choice = input(f"Equip/use {item.name}? (y/n)> "). strip().lower()
                if choice.startswith('y'):
                    if isinstance(item, type(self.player.weapon)):
                        self.player.weapon = item
                    elif isinstance(item, type(self.player.passive)):
                        self.player.passive = item
                    else:
                        if len(self.player.active_items) < self.player.active_slots:
                            self.player.active_items.append(item)
                        else:
                            if len(self.player.active_items) < self.player.active_slots:
                                self.player.active_items.append(item)
                            else:
                                print(f"No active slot free, discarding {item.name}.")
                    self.player_log['items_acquired'] = self.player_log.get('items_acquired', 0) + 1
                    self.player_log['battle_logs'].append(f"Acquired {item.name}.")
                else:
                    print(f"Discarded {item.name}.")

            self.player_log['battle_logs'].append(f"Battle with {[m.name for m in enemies]} won.")
            self.save_system.save_player(self.player, self.player_log)
            return True

        else:
            print("\n>>> YOU DIED <<<")
            self.player_log['battle_logs'].append("Player died. Game OVER.")
            self.save_system.save_player(self.player, self.player_log)
            return False

    def post_battle_gap(self):
        print("\n --- Battle gap: check inventory and save ---")
        self.save_system.save_player(self.player, self.player_log)
        print("Progress saved. Preparing next battle...\n")


