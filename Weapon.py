from Stats import Stats
from Mods import Mods
from DamageTypes import DamageTypes

class Weapon:
    def __init__(self, baseStats: Stats, mods: Mods):
        self.stats = Stats("")
        self.Name = baseStats.Name
        self.ModName = mods.Name
        self.mods = mods
        self.BaseDamage = 0
        self.UnmoddedDamage = 0
        self.BaseDamageMultiplier = 1 + mods.Multiplier["BaseDamage"]
        self.Quantum = 0

        # https://warframe.fandom.com/wiki/Damage#Quantization
        # We need the UnmoddedDamage-Variable for calculating our Quantum
        for entry in DamageTypes().Damage:
            self.UnmoddedDamage = self.UnmoddedDamage + (baseStats.Damage[entry] * self.BaseDamageMultiplier)

        # Set the base damage. The base-damage is needed to calculate additional damage, like "Toxin" on "Braton Prime" when using "Infected Clip"
        for entry in DamageTypes().Damage:
            self.stats.Damage[entry] = round(baseStats.Damage[entry] * self.BaseDamageMultiplier, 1)
            self.BaseDamage = self.BaseDamage + round(baseStats.Damage[entry],0)

        # Add and sum toxin, slash and stuff (e.g. Calculating Toxin Damage for a weapon that got Toxin Damage through a mod, like "Infected Clip" on "Braton Prime")
        for entry in DamageTypes().Damage:
            self.stats.Damage[entry] = self.stats.Damage[entry] + (self.BaseDamage * mods.Multiplier[entry])

        for entry in DamageTypes().Additionals:
            if entry == "FactionDamage":
                self.stats.Damage[entry] = round(baseStats.Damage[entry] + mods.Multiplier[entry], 1)
            else:
                self.stats.Damage[entry] = round(baseStats.Damage[entry] * (1 + mods.Multiplier[entry]), 1)

        for entry in DamageTypes().SpecialMods:
            self.stats.Damage[entry] = mods.Multiplier[entry]

        self.Quantum = float(self.UnmoddedDamage / 16)

    # see https://warframe.fandom.com/wiki/Damage#Damage_Calculation
    def QuantizedDamageType(self, type: str):
        return round((self.stats.Damage[type] / self.Quantum) * self.BaseDamageMultiplier, 0) * self.Quantum

    def ShowStats(self, showProcs: bool):
        string = ""
        for entry in DamageTypes().Multiplier:
            if entry == "BaseDamage": # We just want to ignore that value. It doesn't show up in warframe either
                continue
            if entry in DamageTypes().Additionals:
                string = string + "\t" + entry + ": " + str(round(self.stats.Damage[entry], 1)) + "\r\n"
            else:
                string = string + "\t" + entry + ": " + str(round(self.stats.Damage[entry] * self.BaseDamageMultiplier, 1)) + "\r\n"

        if showProcs:
            string = string + "\t" + "Approximately " + str(round(self.stats.Damage["Multishot"] * (self.stats.Damage["StatusChance"] / 100), 5)) + " Status Procs per shot with following probability: \r\n"
            procs = self.CalculateProcs()
            for entry in procs.keys():
                string = string + "\t\t" + entry + ": " + str(round(procs[entry], 5)) + " = " + str(round(procs[entry] * self.stats.Damage["Multishot"], 5)) + " Procs\r\n"

        if int(self.stats.Damage["HunterMunition"]) == 1:
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
