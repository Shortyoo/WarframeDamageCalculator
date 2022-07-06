from DamageTypes import DamageTypes
import configparser

class Stats:
    def __init__(self, name: str):
        self.Damage = {}
        for entry in DamageTypes().Multiplier:
            self.Damage[entry] = 0

        self.Name = name

    def loadWeapon(name: str):
        weaponParser = configparser.ConfigParser()
        weaponParser.read("Weapons/"+name+".ini")
        weaponStats = Stats(name)
        for entry in DamageTypes().Multiplier:
            if entry == "BaseDamage" or entry == "FactionDamage":
                continue
            weaponStats.Damage[entry] = float(weaponParser["Weapon"][entry])
        return weaponStats
