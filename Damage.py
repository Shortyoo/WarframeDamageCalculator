from Weapon import Weapon
from DamageTypes import DamageTypes
from Enemy import Enemy
from Armor import Armor

class Damage:
    def __init__(self, weapon: Weapon, enemy: Enemy):
        self.weapon = weapon
        self.enemy = enemy

    def DamageModifierArmor(self, type):
        # https://warframe.fandom.com/wiki/Damage/Corrosive_Damage
        armorReduction = self.CalculateArmorReduction()
        armorValue = self.enemy.Armor * (armorReduction)

        # https://warframe.fandom.com/wiki/Damage#Damage_Calculation
        #print(type+"modifier: "+str((300 / (300 + armorValue * (1 - self.enemy.armor.ArmorMultiplier[type]))) * (1 + self.enemy.armor.ArmorMultiplier[type]) * (1 + self.enemy.health.HealthMultiplier[type])))
        return (300 / (300 + armorValue * (1 - self.enemy.armor.ArmorMultiplier[type]))) * (1 + self.enemy.armor.ArmorMultiplier[type]) * (1 + self.enemy.health.HealthMultiplier[type])

    def GeneralDamageAmplifier(self):
        headshot = 0 # we aim for the head
        critDmg = 1#self.weapon.stats.Damage["CritDamage"]#(1 + ((self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]))
        return critDmg * (1 + headshot) * (1 + self.weapon.stats.Damage["FactionDamage"])

    def DamageModifierShield(self, entry):
        return (1 + self.enemy.shield.ShieldMultiplier[entry])

    def SubtractDamage(self, damage, multishot, attribute):
        while multishot > 0 and attribute > 0:
            attribute = attribute - damage
            multishot = multishot - 1
        # Maybe we have Multishot 12.2, we calculated 12 rounds but I want to consider that leftover 0.2 as well
        if multishot < 1 and attribute > 0:
            attribute = attribute - (damage * multishot)

        return(multishot, attribute)

    def ShootEnemy(self):
        shots = 0
        while self.enemy.remainingHP > 0:
            shots = shots + 1
            # Destroy shield before attacking HP
            multishot = self.weapon.stats.Damage["Multishot"]
            if self.enemy.remainingShield > 0:
                damage = self.CalculateSingleshot(self.DamageModifierShield)
                #print("In ShootEnemy: "+str(damage))
                (multishot, self.enemy.remainingShield) = self.SubtractDamage(damage, multishot, self.enemy.remainingShield)
                if self.enemy.remainingShield < 0:
                    damage = self.CalculateSingleshot(self.DamageModifierArmor)
                    (multishot, self.enemy.remainingHP) = self.SubtractDamage(damage, multishot, self.enemy.remainingHP)
            else:
                damage = self.CalculateSingleshot(self.DamageModifierArmor)
                #print("Damage: "+str(damage) + " HP: " + str(self.enemy.remainingHP))
                #print("Multishot: "+str(multishot))
                (multishot, self.enemy.remainingHP) = self.SubtractDamage(damage, multishot, self.enemy.remainingHP)
                #print("Remaining hP: "+ str(self.enemy.remainingHP))

        self.enemy.remainingHP = self.enemy.HP
        self.enemy.remainingShield = self.enemy.remainingShield

        print("It took: " + str(shots) + " shots to kill " + self.enemy.Name)

    def CalculateSingleshot(self, function):
        self.singleDamage = {}
        self.totalDamage = 0
        for entry in DamageTypes().Damage:
            # https://warframe.fandom.com/wiki/Damage#Generalized_Damage_Modifier explains * self.GeneralDamageAmplifier()
            # https://warframe.fandom.com/wiki/Damage#Total_Damage explains Quantiziation
            self.singleDamage[entry] = self.weapon.QuantizedDamageType(entry) * function(entry)
            #print(entry + "-Damage: " + str(self.singleDamage[entry]))
            self.totalDamage = self.totalDamage + self.singleDamage[entry]

        self.totalDamage = self.totalDamage * self.GeneralDamageAmplifier()
        print("Total: "+ str(self.totalDamage))
        return round(self.totalDamage, 0)

    def CalculateRawDamage(self):
        return (self.CalculateSingleshot(self.DamageModifierShield), self.CalculateSingleshot(self.DamageModifierArmor))

    def CalculateRawDamageMultiShot(self):
        return self.CalculateSingleshot(self.DamageModifierArmor) * self.weapon.stats.Damage["Multishot"]

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
