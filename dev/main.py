from sys import exception
import cmd2
from player import *
from SaveSystem import *
from combat import *
from item_registry import *

class GameShell(cmd2.Cmd):
    prompt = ">> "

    def __init__(self):
        super().__init__()
        self.player = None
        self.player_log = None
        self.combat_manager = None
        self.save_system = None
    
    def do_slots(self, arg):
        existing = SaveSystem.list_slots()
        if existing:
            self.poutput(f"Existing slots: {existing}")
        else:
            self.poutput("No save slots found.")

    def do_delete(self, arg):
        try:
            slot = int(arg.strip())
            ss = SaveSystem(slot)
            ss.delete_slot()
            self.poutput(f"Slot {slot} deleted.")
        except Exception as e:
            self.poutput(f"Error: {e}")

    def do_start(self, arg):
        try:
            slot = int(arg.strip())
            self.save_system = SaveSystem(slot)
            loaded = self.save_system.load_player()
            if loaded in None:
                self.poutput("Starting a new Game")
                init_weapon = item_registry["Basic Sword"]
                import copy
                weapon = copy.deepcopy(init_weapon)
                self.player = Player(name="Normal Person", hp=100, weapon = weapon, passive = None)
                self.player_log = {"time_played": 0, "battle_logs": [], "items_acquired": 0}

            else:
                self.player, self.player_log = loaded
                self.poutput(f"Loaded game for player {self.player.name}.")

            self.combat_manager = CombatManager(self.player, self.save_system, self.player_log)
            self.combat_manager.start_game()
        except Exception as e:
            self.poutput(f"Error: {e}")

    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    shell = GameShell()
    shell.cmdloop()

