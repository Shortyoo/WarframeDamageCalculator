from Weapon import Weapon
from DamageTypes import DamageTypes
from Enemy import Enemy
from DamageResistances import DamageResistances
from Status import Status
import random

class Damage:
    def __init__(self, weapon: Weapon, enemy: Enemy):
        self.weapon = weapon
        self.enemy = enemy
        self.DamageResistanceInstance = DamageResistances()
        self.DamageTypesInstance = DamageTypes()

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

    def CalculateGuaranteedCritTier(self):
        critChance = self.weapon.stats.Damage["CritChance"]
        # Example:
        # CritChance = 180%. 180 / 100 = 1.8 => 1. So we're in yellow crit here
        # Crit Chance = 68% => 68/100 = 0 => No guaranteed crit
        GuaranteedCritTier = int(critChance / 100)
        return GuaranteedCritTier

    # see https://warframe.fandom.com/wiki/Critical_Hit#Crit_Tiers
    def CalculateCritMultiplier(self):
        critChance = self.weapon.stats.Damage["CritChance"]
        critDamage = self.weapon.stats.Damage["CritDamage"]
        # Example:
        # CritChance = 180%. 180 / 100 = 1.8 => 1. So we're definitely in yellow crit here
        # Crit Chance = 68% => 68/100 = 0.
        GuaranteedCritTier = self.CalculateGuaranteedCritTier()

        # CritChance 180% -> get those 80%
        critChance -= int(critChance/100)*100

        CritTier = GuaranteedCritTier + self.ProbabilityCheck(critChance)

        CritTierMulti = 1 + CritTier * (critDamage - 1)

        #critDmg = self.weapon.stats.Damage["CritDamage"]
        #critDmg = (1 + ((self.weapon.stats.Damage["CritChance"] / 100) * self.weapon.stats.Damage["CritDamage"]))
        return CritTierMulti

    def GeneralDamageAmplifier(self):
        headshot = 0 # we aim for the head
        critDmg = self.CalculateCritMultiplier()
        return critDmg * (1 + headshot) * (1 + self.weapon.stats.Damage["FactionDamage"])

    def DamageModifierShield(self, entry):
        damageTypeModifier = self.DamageResistanceInstance.GetMultiplier(entry, self.enemy.shieldType)
        statusModifier = 0
        if self.enemy.status.Status["Magnetic"] > 0:
            statusModifier = (1 + (0.25 * (self.enemy.status.Status["Magnetic"] - 1)))

        return (1 + damageTypeModifier + statusModifier)

    def ShootEnemy(self):
        shots = 0
        enemyOldStatus = Status(self.enemy.status.Status)
        while self.enemy.remainingHealth > 0:
            shots = shots + 1
            multishot = self.weapon.stats.Damage["Multishot"]

            while multishot >= 1:
                # Destroy shield before attacking Health
                if self.enemy.remainingShield > 0:
                    damage = self.CalculateSingleshot(self.DamageModifierShield)
                    # Toxin Damage bypasses "Shield" and "Proto Shield". So we want to deal diect damage to health with it:
                    # see https://warframe.fandom.com/wiki/Damage/Overview_Table#All_
                    if self.enemy.shieldType == "Proto Shield" or self.enemy.shieldType == "Shield":
                        damageToHealth = round(self.weapon.QuantizedDamageType("Toxin", self.GetAdditionalDamageMultipliers()) * self.DamageModifierArmor("Toxin"), 0)
                        self.enemy.remainingHealth = self.enemy.remainingHealth - damageToHealth
                    self.enemy.remainingShield -= damage
                # Damage to Health
                else:
                    damage = self.CalculateSingleshot(self.DamageModifierArmor)
                    self.enemy.remainingHealth -= damage

                self.ApplyStatusProcs()
                multishot -= 1

        self.enemy.remainingHealth = self.enemy.health
        self.enemy.remainingShield = self.enemy.remainingShield
        # reset if we want to call "ShootEnemy" again
        self.enemy.status = enemyOldStatus
        print("It took: " + str(shots) + " shots to kill " + self.enemy.Name)

    def GetAdditionalDamageMultipliers(self):
        additionalMultiplier = 0
        galvanizedStacks = 0 # from 0-3 or 0-2, depending on the mod/weapon
        galvanizedDamagePerStack = 0 #ranging from 0.03 - 0.4
        statusCount = self.enemy.GetStatusCount()

        for galvanizedMod in self.DamageTypesInstance.GalvanizedMods:
            if self.weapon.mods.Multiplier[galvanizedMod] > 0:
                galvanizedDamagePerStack = self.weapon.mods.Multiplier[self.DamageTypesInstance.DamagePerStack]
                galvanizedStacks = self.weapon.mods.Multiplier[galvanizedMod]

                additionalMultiplier = additionalMultiplier + (statusCount * galvanizedDamagePerStack * galvanizedStacks)
                break # There can be just one galvanized mod. No need to look for other ones
        return additionalMultiplier

    # Calculatates whether we're lucky to get an additional status/crit/multishot etc
    # The passed value is multilpied 10 for the following reason:
    # Suppose we have a 20.2% Crit-Chance. We dont want to miss out on those 0.2%! So we increase it to
    # 202, and adjust our randint ranging from 1,1000 instead of 1,100
    def ProbabilityCheck(self, valueToCompareWith: int):
        rand = random.Random()
        randValue = rand.randint(1,1000)
        if randValue <= (valueToCompareWith * 10):
            return 1
        return 0

    def ApplyStatusProcs(self):
        statusChance = self.weapon.stats.Damage["StatusChance"]
        guaranteedProcs = int(statusChance / 100) # i.e. Status Chance is 120%, we will have 1 guaranteed proc
        probabilityForAdditionalProc = statusChance - (guaranteedProcs*100) # subtract the guaranteedProcs
        # Calculate which procs can occur which their %-chance
        procProbability = self.weapon.CalculateProcs()
        damageTypes = []
        damageWeights = []
        # prepare variabled
        for entry in procProbability.keys():
            damageTypes.append(entry)
            damageWeights.append(procProbability[entry])

        procCount = guaranteedProcs + self.ProbabilityCheck(probabilityForAdditionalProc)

        # choose a weighted but randomly chosen damageType thats available and
        # apply it to the enemy
        rand = random.Random()
        for i in range(0, procCount):
            damageType = rand.choices(damageTypes, weights = damageWeights, k=1)[0]
            self.enemy.status.Status[damageType] += 1
            if self.enemy.status.Status[damageType] > 10 and damageType != "Slash":
                self.enemy.status.Status[damageType] = 10
            #print(damageType+" proc issued!")

        self.enemy.ValidateProcs()

    # Calculates the damage of a single bullet without taking crits into account
    # function: A function to calculate the DamageModifier, i.e. DamageModifierShield or DamageModifierArmor
    def CalculateSingleshotWithoutCrit(self, function):
        self.singleDamage = {}
        self.totalDamage = 0
        for entry in self.DamageTypesInstance.Damage:
            # https://warframe.fandom.com/wiki/Damage#Total_Damage explains Quantiziation
            self.singleDamage[entry] = self.weapon.QuantizedDamageType(entry, self.GetAdditionalDamageMultipliers()) * function(entry)
            self.totalDamage = self.totalDamage + self.singleDamage[entry]
        return self.totalDamage

    # Calculates the damage of a single bullet WITH takin crits into account
    # function: A function to calculate the DamageModifier, i.e. DamageModifierShield or DamageModifierArmor
    def CalculateSingleshot(self, function):
        # https://warframe.fandom.com/wiki/Damage#Generalized_Damage_Modifier explains * self.GeneralDamageAmplifier()
        # Somehow, they say you have to calculate the crit chance for EACH damage type. But that's bs.
        # Either every damagetype of a bullet crit or none. But not just a single one.
        return round(self.CalculateSingleshotWithoutCrit(function) * self.GeneralDamageAmplifier(), 0)

    def PrintRawDamage(self):
        dmg = self.CalculateRawDamage()

        firerate = self.weapon.stats.Damage["FireRate"]
        magsize = self.weapon.stats.Damage["MagSize"]
        DPS = magsize / firerate
        # If DPS < 1, means that we cant even fire for 1 second.
        # DPS > 1 means we could fire for more than 1 sec, but we want the exact value for 1 sec
        if DPS > 1:
            DPS = self.weapon.stats.Damage["FireRate"]

        if self.enemy.shieldType != "None":
            print(self.BuildString() + " Min-Damage against Shield: {:,.2f}".format(dmg[0][0]))
            print(self.BuildString() + " Max-Damage against Shield: {:,.2f}".format(dmg[0][1]))
            print(self.BuildString() + " Average-Damage against Shield: {:,.2f}".format(dmg[0][2]))
            print(self.BuildString() + " Average-DPS against Shield: {:,.2f}".format(dmg[0][2] * DPS))
        print(self.BuildString() + " Min-Damage against Health: {:,.2f}".format(dmg[1][0]))
        print(self.BuildString() + " Max-Damage against Health: {:,.2f}".format(dmg[1][1]))
        print(self.BuildString() + " Average-Damage against Health: {:,.2f}".format(dmg[1][2]))
        print(self.BuildString() + " Average-DPS against Health: {:,.2f}".format(dmg[1][2] * DPS))

    # Calculates the raw damage for Shield and Health (through armor)
    def CalculateRawDamage(self):
        shieldMinMaxAvgDamage = (0,0,0)
        armorMinMaxAvgDamage = (0,0,0)
        critChance = self.weapon.stats.Damage["CritChance"]
        critDamage = self.weapon.stats.Damage["CritDamage"]
        guaranteedCrits = round((critChance+49.9)/100,0)
        CritMulti = 1 + guaranteedCrits * (critDamage - 1)
        enemyFormerStatus = Status(self.enemy.status.Status)
        enemyModifiedStatus = Status(self.enemy.status.Status)
        # Add a status proc for every damage type occuring
        for entry in self.DamageTypesInstance.Damage:
            if self.weapon.stats.Damage[entry] > 0:
                if entry != "Slash":
                    enemyModifiedStatus.Status[entry] = 10
                else:
                    enemyModifiedStatus.Status[entry] += 1

        if self.enemy.shieldType != "None":
            self.enemy.status = enemyFormerStatus
            shieldMinDamage = round(self.CalculateSingleshotWithoutCrit(self.DamageModifierShield), 0)
            self.enemy.status = enemyModifiedStatus
            shieldMaxDamage = round(self.CalculateSingleshotWithoutCrit(self.DamageModifierShield), 0) * CritMulti
            shieldAvgDamage = shieldMinDamage * ((critChance/100) * critDamage)
            shieldMinMaxAvgDamage = (shieldMinDamage, shieldMaxDamage, shieldAvgDamage)

        self.enemy.status = enemyFormerStatus
        armorMinDamage = round(self.CalculateSingleshotWithoutCrit(self.DamageModifierArmor), 0)
        self.enemy.status = enemyModifiedStatus
        armorMaxDamage = round(self.CalculateSingleshotWithoutCrit(self.DamageModifierShield), 0) * CritMulti
        armorAvgDamage = armorMinDamage * ((critChance/100) * critDamage)
        armorMinMaxAvgDamage = (armorMinDamage, armorMaxDamage, armorAvgDamage)
        self.enemy.status = enemyFormerStatus
        return (shieldMinMaxAvgDamage, armorMinMaxAvgDamage)

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
        slashDamagePerTick = 0.35 * self.weapon.stats.Damage["Slash"] * self.GeneralDamageAmplifier() * (1 + self.DamageResistances.GetMutliplier("Slash", self.enemy.armorType))

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
