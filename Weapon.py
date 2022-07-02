from Stats import Stats
from Mods import Mods
from DamageTypes import DamageTypes

class Weapon:
    def __init__(self, baseStats: Stats, mods: Mods):
        self.stats = Stats()
        for entry in DamageTypes().Multiplier:
            self.stats.Damage[entry] = round(baseStats.Damage[entry] * mods.Multiplier[entry] * mods.Multiplier["BaseDamage"], 1)

        self.stats.Damage.pop("BaseDamage")
        self.Quantum = (baseStats.BaseDamage() * mods.Multiplier["BaseDamage"]) / 16

    def QuantizedDamageType(self, type: str):
        return round(self.stats.Damage[type] / self.Quantum, 0) * self.Quantum
