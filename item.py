# item.py

from dice import roll_d20, interpret_roll
from effects import BleedEffect, FireEffect, StunEffect, RegenEffect, DamageBonusEffect, DefenseReductionEffect
# ↑ 반드시 'effects.py' 파일로 위에서 제공한 Effect/StatusEffect 클래스 구현이 존재해야 함

def create_effect_instance(effect_dict):
    if not effect_dict:
        return None

    type_ = effect_dict.get("type")
    value = effect_dict.get("value")

    if type_ == "bleed":
        return BleedEffect(damage_per_turn=value, duration=3)
    elif type_ == "fire":
        return FireEffect(damage_per_turn=value, duration=3)
    elif type_ == "stun":
        return StunEffect(duraiton=1)
    elif type_ == "regen":
        return RegenEffect(heal_per_turn=value, duration=3)
    elif type_ == "attack_bonus":
        return DamageBonusEffect(bonus=value)
    elif type_ == "reduce":
        return DefenseReductionEffect(bonus=value)
    return None


class Item:
    def __init__(self, name, description, rarity="common", effect=None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.effect = effect

    def use(self, player):
        print(f"You Used {self.name}!")

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'description': self.description,
            'rarity': self.rarity,
            'effect': self.effect
        }

    def __str__(self):
        effct = f", Effect : {self.effect}" if self.effect else ""
        return f"{self.name} (({self.rarity}) - {self.description}{effct})"


class Weapon(Item):
    def __init__(self, name, description, damage, rarity="common", effect=None):
        super().__init__(name, description, rarity, effect)
        self.damage = damage

    def get_status_effect(self):
        return create_effect_instance(self.effect)


class Passive(Item):
    def __init__(self, name, description, deffend, rarity="common", effect=None):
        super().__init__(name, description, rarity, effect)
        self.deffend = deffend

    def use(self, player):
        effect = create_effect_instance(self.effect)
        if effect:
            player.apply_temp_effect(effect)  # 이 함수는 플레이어 클래스에서 정의되어야 함


class Active(Item):
    def __init__(self, name, description, max_uses, rarity="common", effect=None):
        super().__init__(name, description, rarity, effect)
        self.max_uses = max_uses
        self.remaining = max_uses

    def use(self, player):
        if self.remaining <= 0:
            print(f"You Can't Use {self.name} Anymore!")
            return False

        super().use(player)
        print(f"REMAIN : {self.remaining - 1} out of {self.max_uses}")

        roll = roll_d20()
        result = interpret_roll(roll)
        self.activate_effect(player, result)

        self.remaining -= 1
        if self.remaining <= 0:
            print(f"{self.name} Has Been Used Up.")
            return True
        return False

    def activate_effect(self, player, result):
        effect = create_effect_instance(self.effect)
        if effect:
            if hasattr(effect, "on_turn"):
                player.add_status(effect)
            else:
                player.apply_temp_effect(effect)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'max_uses': self.max_uses,
            'remaining_uses': self.remaining
        })
        return base
