from player import *
from SaveSystem import *
from combat import *
from item_registry import *
import cmd2
import copy

class GameShell(cmd2.Cmd):
    prompt = ">> "
    intro = "Type any of the following commands:\n" \
            "  slots\n" \
            "  delete <slot>\n" \
            "  start <slot>\n" \
            "  exit\n"

    def __init__(self):
        super().__init__()
        self.player = None
        self.player_log = None
        self.combat_manager = None
        self.save_system = None

#    def preloop(self):
#        super().preloop()

#    def postcmd(self, stop: bool, line: str) -> bool:
#        return stop
        
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

            if loaded is None:
                self.poutput("Starting a new game.")
                weapon = copy.deepcopy(item_registry["Basic Sword"])
                self.player = Player(name="YOU", hp=100, weapon=weapon, passive=None)
                self.player_log = {"time_played":0, "battle_logs":[], "items_acquired":0}
            else:
                self.player, self.player_log = loaded
                self.poutput(f"Loaded game for player {self.player.name}.")

            self.combat_manager = CombatManager(self.player, self.save_system, self.player_log)
            survived = self.combat_manager.start_game()

            if not survived:
                self.poutput("\n=== Game Over ===")
                for entry in self.player_log["battle_logs"]:
                    self.poutput(entry)
                choice = input("Continue from this slot? (y/n)> ").strip().lower()
                if choice.startswith("y"):
                    return self.do_start(arg)
                else:
                    self.poutput("Returning to main menu.")
        except Exception as e:
            self.poutput(f"Error: {e}")

    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    shell = GameShell()
    shell.cmdloop()

