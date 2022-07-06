from Status import Status
import configparser
from DamageTypes import DamageTypes

class Enemy:
    def __init__(self, health: float, shield: float, armor: float, name: str, healthType: str, shieldType: str, armorType: str):
        self.health = float(health)
        self.shield = float(shield)
        self.armor = float(armor)
        self.Name = str(name)
        self.healthType = str(healthType)
        self.shieldType = str(shieldType)
        self.armorType = str(armorType)
        self.remainingHealth = float(health)
        self.remainingShield = float(shield)
        self.status = Status()

        #print("Remaining Shield: " + str(self.remainingShield))
        #print("Armor: " + str(self.Armor))
        #print("Remaining health: " + str(self.remainingHealth))

    def loadEnemy(name: str):
        enemyParser = configparser.ConfigParser()
        enemyParser.read("Enemies/" + name + ".ini")

        health = int(enemyParser["Base"]["Health"])
        armor = int(enemyParser["Base"]["Armor"])
        shield = int(enemyParser["Base"]["Shield"])
        baseLevel = int(enemyParser["Base"]["BaseLevel"])
        level = int(enemyParser["Base"]["Level"])
        name = str(enemyParser["Base"]["Name"])
        healthType = str(enemyParser["Base"]["HealthType"])
        shieldType = str(enemyParser["Base"]["ShieldType"])
        armorType = str(enemyParser["Base"]["ArmorType"])

        if level - baseLevel < 70:
            armor = round(armor * (1 + 0.0005 * (level - baseLevel)**1.75), 2)
            health = round(health * (1 + 0.015 * (level - baseLevel)**2), 2)
            shield = round(shield * (1 + 0.02*(level - baseLevel)**1.75), 2)
        else:
            armor = round(armor * (1 + 0.4 * (level - baseLevel)**0.75), 2)
            health = round(health * (1 + (24*(5**0.5)/5) * (level - baseLevel) ** 0.5), 2)
            shield = round(shield * (1 + 1.6*(level - baseLevel)**0.75), 2)

        if int(enemyParser["Base"]["SteelPath"]) == 1:
            # at first, add the armor value that it gains from + 100 levels
            # https://warframe.fandom.com/wiki/The_Steel_Path
            health = health * 2.5
            shield = shield * 2.5
            armor = armor * 2.5

        return Enemy(health, shield, armor, name, healthType, shieldType, armorType)
