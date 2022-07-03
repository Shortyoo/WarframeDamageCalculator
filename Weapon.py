from Stats import Stats
from Mods import Mods
from DamageTypes import DamageTypes

class Weapon:
    def __init__(self, baseStats: Stats, mods: Mods):
        self.stats = Stats("")
        self.Name = baseStats.Name
        self.BaseDamage = 0
        self.UnmoddedDamage = 0

        for entry in DamageTypes().Damage:
            self.UnmoddedDamage = self.UnmoddedDamage + baseStats.Damage[entry]

        # Set the base damage
        for entry in DamageTypes().Damage:
            self.stats.Damage[entry] = round(baseStats.Damage[entry] * (1 + mods.Multiplier["BaseDamage"]), 1)
            self.BaseDamage = self.BaseDamage + self.stats.Damage[entry]

        for entry in DamageTypes().Additionals:
            self.stats.Damage[entry] = round(baseStats.Damage[entry] * (1 + mods.Multiplier[entry]), 1)

        # Add and sum toxin, slash and stuff
        for entry in DamageTypes().Damage:
            #if self.stats.Damage[entry] > 0:
            self.stats.Damage[entry] = self.stats.Damage[entry] + (self.UnmoddedDamage * mods.Multiplier[entry] * (1 + mods.Multiplier["BaseDamage"]))

    def ModdedBaseDamage(self):
        damage = 0
        for entry in DamageTypes().Damage:
            damage = damage + self.stats.Damage[entry]
        return damage

    def QuantizedDamageType(self, type: str):
        self.Quantum = self.ModdedBaseDamage() / 16
        return round(self.stats.Damage[type] / self.Quantum, 0) * self.Quantum

    def ShowStats(self):
        string = ""
        for entry in DamageTypes().Multiplier:
            if entry == "BaseDamage":
                continue
            string = string + "\t" + entry + ": " + str(round(self.stats.Damage[entry], 1)) + "\r\n"
        return string

    def CalculateProcs(self):
        probability = {}
        for entry in DamageTypes().Damage:
            if self.stats.Damage[entry] > 0:
                probability[entry] = 0

        # iterate through all possibilities
        for key in probability.keys():
            probability[key] = self.stats.Damage[key] / self.ModdedBaseDamage()

        return probability
