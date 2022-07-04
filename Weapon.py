from Stats import Stats
from Mods import Mods
from DamageTypes import DamageTypes

class Weapon:
    def __init__(self, baseStats: Stats, mods: Mods):
        self.stats = Stats("")
        self.Name = baseStats.Name
        self.ModName = mods.Name
        self.BaseDamage = 0
        self.UnmoddedDamage = 0

        for entry in DamageTypes().Damage:
            self.UnmoddedDamage = self.UnmoddedDamage + baseStats.Damage[entry]

        # Set the base damage
        for entry in DamageTypes().Damage:
            self.stats.Damage[entry] = round(baseStats.Damage[entry] * (1 + mods.Multiplier["BaseDamage"]), 1)
            self.BaseDamage = self.BaseDamage + self.stats.Damage[entry]

        for entry in DamageTypes().Additionals:
            if entry == "FactionDamage":
                self.stats.Damage[entry] = round(baseStats.Damage[entry] + mods.Multiplier[entry], 1)
            else:
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

    def ShowStats(self, showProcs: bool, procHunterMunition: bool):
        string = ""
        for entry in DamageTypes().Multiplier:
            if entry == "BaseDamage":
                continue
            string = string + "\t" + entry + ": " + str(round(self.stats.Damage[entry], 1)) + "\r\n"

        string = string + "\t" + "Approximately " + str(round(self.stats.Damage["Multishot"] * (self.stats.Damage["StatusChance"] / 100), 5)) + " Status Procs per shot with following probability: \r\n"

        if showProcs:
            procs = self.CalculateProcs()
            for entry in procs.keys():
                string = string + "\t\t" + entry + ": " + str(round(procs[entry], 5)) + " = " + str(round(procs[entry] * self.stats.Damage["Multishot"], 5)) + " Procs\r\n"

        if procHunterMunition:
            string = string + "\t Hunter Munitions proc " + str(round(self.stats.Damage["Multishot"] * (self.stats.Damage["CritChance"] / 100) * 0.3, 2)) + " times Slash"


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
