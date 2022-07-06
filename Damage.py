from Weapon import Weapon
from DamageTypes import DamageTypes
from Enemy import Enemy
from DamageResistances import DamageResistances

class Damage:
    def __init__(self, weapon: Weapon, enemy: Enemy):
        self.weapon = weapon
        self.enemy = enemy
        self.DamageResistanceInstance = DamageResistances()

    def DamageModifierArmor(self, type):
        # see https://warframe.fandom.com/wiki/Damage/Corrosive_Damage
        armorReduction = self.CalculateArmorReduction()
        armorValue = self.enemy.armor * (armorReduction)
        # see https://warframe.fandom.com/wiki/Damage#Armored_Enemies
        # Variable names are shitty, but they're equal to above's link formula
        AR = armorValue
        AM = self.DamageResistanceInstance.GetMultiplier(type, self.enemy.armorType)
        HM = self.DamageResistanceInstance.GetMultiplier(type,self.enemy.healthType)

        return (300 / (300 + AR * (1 - AM))) * (1 + AM) * (1 + HM)

    def GeneralDamageAmplifier(self):
        headshot = 0 # we aim for the head
        critDmg = 1#self.weapon.stats.Damage["CritDamage"]#(1 + ((self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]))
        return critDmg * (1 + headshot) * (1 + self.weapon.stats.Damage["FactionDamage"])

    def DamageModifierShield(self, entry):
        return (1 + self.DamageResistanceInstance.GetMultiplier(entry, self.enemy.shieldType))

    def SubtractDamage(self, damage, multishot, attribute):
        while multishot > 0 and attribute > 0:
            attribute = attribute - damage
            multishot = multishot - 1
        # Maybe we have Multishot 12.2, we calculated 12 rounds but I want to consider that leftover 0.2 as well with that exact weight of 0.2
        if multishot < 1 and attribute > 0:
            attribute = attribute - (damage * multishot)

        return(multishot, attribute)

    def ShootEnemy(self):
        shots = 0
        while self.enemy.remainingHealth > 0:
            shots = shots + 1
            multishot = self.weapon.stats.Damage["Multishot"]
            # Destroy shield before attacking Health
            if self.enemy.remainingShield > 0:
                damage = self.CalculateSingleshot(self.DamageModifierShield)
                # Toxin Damage bypasses "Shield" and "Proto Shield". So we want to deal diect damage to health with it:
                # see https://warframe.fandom.com/wiki/Damage/Overview_Table#All_
                if self.enemy.shieldType == "Proto Shield" or self.enemy.shieldType == "Shield":
                    damageToHealth = round(self.weapon.QuantizedDamageType("Toxin") * self.DamageModifierArmor("Toxin"), 0)
                    self.enemy.remainingHealth = self.enemy.remainingHealth - damageToHealth
                (multishot, self.enemy.remainingShield) = self.SubtractDamage(damage, multishot, self.enemy.remainingShield)
                if self.enemy.remainingShield < 0:
                    damage = self.CalculateSingleshot(self.DamageModifierArmor)
                    (multishot, self.enemy.remainingHealth) = self.SubtractDamage(damage, multishot, self.enemy.remainingHealth)
            # Damage to Health
            else:
                damage = self.CalculateSingleshot(self.DamageModifierArmor)
                (multishot, self.enemy.remainingHealth) = self.SubtractDamage(damage, multishot, self.enemy.remainingHealth)

        self.enemy.remainingHealth = self.enemy.health
        self.enemy.remainingShield = self.enemy.remainingShield

        print("It took: " + str(shots) + " shots to kill " + self.enemy.Name)

    # Calculates the damage of a single bullet
    # function: A function to calculate the DamageModifier, i.e. DamageModifierShield or DamageModifierArmor
    def CalculateSingleshot(self, function):
        self.singleDamage = {}
        self.totalDamage = 0
        for entry in DamageTypes().Damage:

            # https://warframe.fandom.com/wiki/Damage#Total_Damage explains Quantiziation
            self.singleDamage[entry] = self.weapon.QuantizedDamageType(entry) * function(entry)
            self.totalDamage = self.totalDamage + self.singleDamage[entry]

        # https://warframe.fandom.com/wiki/Damage#Generalized_Damage_Modifier explains * self.GeneralDamageAmplifier()
        self.totalDamage = self.totalDamage * self.GeneralDamageAmplifier()
        return round(self.totalDamage, 0)

    # Calculates the raw damage for Shield and Health (through armor)
    def CalculateRawDamage(self):
        return (self.CalculateSingleshot(self.DamageModifierShield), self.CalculateSingleshot(self.DamageModifierArmor))

    # Just mulitplies the RawDamage with the Multishot-Value
    def CalculateRawDamageMultiShot(self):
        return self.CalculateSingleshot(self.DamageModifierArmor) * self.weapon.stats.Damage["Multishot"]

    # Not a real link, but rather collected information on what strips armor
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
        slashDamagePerTick = 0.35 * self.weapon.stats.Damage["Slash"] * (1 + self.weapon.stats.Damage["FactionDamage"]) * (1 + (self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]) * (1 + headshot) * (1 + self.DamageResistances.GetMutliplier("Slash", self.enemy.armorType))

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
