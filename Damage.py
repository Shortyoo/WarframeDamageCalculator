from Weapon import Weapon
from DamageTypes import DamageTypes
from Enemy import Enemy

class Damage:
    def __init__(self, weapon: Weapon, enemy: Enemy):
        self.weapon = weapon
        self.enemy = enemy

    def DamageModifier(self, str):
        armorReduction = 0 # we are not counting in corrosive procs so for
        headshot = 1 # we aim for the head
        return (300 / (300 + self.enemy.armor.ArmorMultiplier[str] * (1 - armorReduction))) * (1 + armorReduction) * (1 + self.enemy.health.HealthMultiplier[str]) * (1 + (self.weapon.stats.Damage["CritChance"] * self.weapon.stats.Damage["CritDamage"])) * (1 + self.weapon.stats.Damage["FactionDamage"]) * (1 + headshot)

    def CalculateSingleshot(self):
        self.singleDamage = {}
        self.totalDamage = 0
        for entry in DamageTypes().Damage:
            self.singleDamage[entry] = self.weapon.QuantizedDamageType(entry) * self.DamageModifier(entry)
            self.totalDamage = self.totalDamage + self.singleDamage[entry]
        return self.totalDamage

    def CalculateMultishot(self):
        return self.CalculateSingleshot() * self.weapon.stats.Damage["Multishot"]
