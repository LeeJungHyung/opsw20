class Mob:
    def __init__(self, name, hp, attack, defense, drops):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.drops = drops

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage = max(0, amount - self.defense)
        self.hp -= damage
        print(f"{self.name} has taken {damage} damage. Remaining HP : {self.hp}")

    def attack_target(self, target):
        print(f"{self.name} is attacking {target.name}!")
        target.take_damage(self.attack)

class EliteMob(Mob):
    def __init__(self, name, hp, attack, defense, drops, skill, skill_power):
        super().__init__(name, hp, attack, defense, drops)
        self.skill = skill
        self.skill_power = skill_power

    def use_skill(self, target):
        print(f"{self.name} is using '{self.skill}'!")
        damage = max(0, self.skill_power - target.get_total_defense())
        target.take_damage(damage)
        print(f"{target.name} takes {damage} damage from skill. Remaining HP: {target.hp}")

    def attack_target(self, target):
        self.use_skill(target)
