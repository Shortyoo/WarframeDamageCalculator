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
        armorReduction = self.CalculateArmorReduction()
        armorValue = self.enemy.Armor * (armorReduction)

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

    def CalculateArmorReduction(self):
        armorReduction = 0

        reductionByHeatProcs = 1
        if self.enemy.status.Status["Heat"] >= 1:
            reductionByHeatProcs = 0.5

        reductionByCorrosiveProjection = 1 - (0.18 * int(self.enemy.status.Status["CorrosiveProjection"]))

        reductionByCorrosiveProcs = 1

        if self.enemy.status.Status["Corrosive"] >= 1:
            reductionByCorrosiveProcs = (1 - (0.2 + 0.06 * int(self.enemy.status.Status["Corrosive"])))

        armorReduction = reductionByHeatProcs * reductionByCorrosiveProcs * reductionByCorrosiveProjection

        armorReduction = round(armorReduction, 5)
        return armorReduction

    def CalculateSlashDamage(self):
        headshot = 1 # we aim for the head
        slashDamagePerTick = 0.35 * self.weapon.stats.Damage["Slash"] * (1 + self.weapon.stats.Damage["FactionDamage"]) * (1 + (self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]) * (1 + headshot) * (1 + self.enemy.armor.ArmorMultiplier["Slash"])

        slashDamagePerTickTimesSlashProcs = slashDamagePerTick
        if self.enemy.status.Status["Slash"] >= 1:
            slashDamagePerTickTimesSlashProcs = slashDamagePerTick * int(self.enemy.status.Status["Slash"])

        slashDamageWithViral = slashDamagePerTickTimesSlashProcs
        # https://warframe.fandom.com/wiki/Damage/Viral_Damage
        if self.enemy.status.Status["Viral"] >= 1:
            slashDamageWithViral = slashDamagePerTick * (2 + (0.25 * (self.enemy.status.Status["Viral"] - 1)))

        return slashDamageWithViral

    def BuildString(self):
        return self.weapon.Name + " with Build: " + self.weapon.ModName + " against: " + self.enemy.Name
