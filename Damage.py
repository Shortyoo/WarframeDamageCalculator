from Weapon import Weapon
from DamageTypes import DamageTypes
from Enemy import Enemy
from Armor import Armor

class Damage:
    def __init__(self, weapon: Weapon, enemy: Enemy):
        self.weapon = weapon
        self.enemy = enemy

    def DamageModifier(self, str):
        # https://warframe.fandom.com/wiki/Damage/Corrosive_Damage
        corrProcs = self.CalculateCorrosiveProcs()
        armorValue = self.enemy.Armor * (1 - corrProcs)

        headshot = 1 # we aim for the head
        # https://warframe.fandom.com/wiki/Damage#Damage_Calculation
        return (300 / (300 + armorValue * (1 - self.enemy.armor.ArmorMultiplier[str]))) * (1 + self.enemy.armor.ArmorMultiplier[str]) * (1 + self.enemy.health.HealthMultiplier[str]) * (1 + ((self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"])) * (1 + self.weapon.stats.Damage["FactionDamage"]) * (1 + headshot)

    def CalculateSingleshot(self):
        self.singleDamage = {}
        self.totalDamage = 0
        for entry in DamageTypes().Damage:
            self.singleDamage[entry] = self.weapon.QuantizedDamageType(entry) * self.DamageModifier(entry)
            self.totalDamage = self.totalDamage + self.singleDamage[entry]
        return self.totalDamage

    def CalculateMultishot(self):
        return self.CalculateSingleshot() * self.weapon.stats.Damage["Multishot"]

    def CalculateCorrosiveProcs(self):
        armorReduction = 0
        procs = self.weapon.CalculateProcs()

        if "Corrosive" in procs:
            if procs["Corrosive"] > 1:
                armorReduction = 0.26 + procs["Corrosive"] * 0.06
                if armorReduction > 0.8:
                    armorReduction = 0.8

        return armorReduction


    def CalculateSlashDamage(self):
        headshot = 1 # we aim for the head
        baseSlash = 0.35 * self.weapon.stats.Damage["Slash"] * (1 + self.weapon.stats.Damage["FactionDamage"]) * (1 + (self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]) * (1 + headshot) * (1 + self.enemy.armor.ArmorMultiplier["Slash"])
        print("baseSlash: " + str(baseSlash))
