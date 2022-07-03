from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
from Enemy import Enemy
from DamageTypes import DamageTypes
import configparser

def loadWeapon(name: str):
    weaponParser = configparser.ConfigParser()
    weaponParser.read("Weapons/"+name+".ini")
    weaponStats = Stats(name)
    for entry in DamageTypes().Multiplier:
        if entry == "BaseDamage" or entry == "FactionDamage":
            continue
        weaponStats.Damage[entry] = float(weaponParser["Weapon"][entry])
    return weaponStats

def loadMod(name: str):
    modParser = configparser.ConfigParser()
    modParser.read("Mods/" + name + ".ini")
    mods = Mods()
    for entry in DamageTypes().Multiplier:
        mods.Multiplier[entry] = float(modParser["Mods"][entry])
    return mods

weaponStatList = []
modStatList = []

calculationParser = configparser.ConfigParser()
calculationParser.read("Calculation.ini")
for entry in calculationParser["Weapons"]:
    weaponStatList.append(loadWeapon(str(calculationParser["Weapons"][entry])))

for entry in calculationParser["Mods"]:
    modStatList.append(loadMod(str(calculationParser["Mods"][entry])))

weapons = []

if len(weaponStatList) != len(modStatList):
    print("Uneven length of weapons and mods!")

else:
    for i in range(0, len(weaponStatList)):
        weapons.append(Weapon(weaponStatList[i], modStatList[i]))

    gunnerArmor = Armor()
    gunnerArmor.ArmorMultiplier["Corrosive"] = 0.75
    gunnerArmor.ArmorMultiplier["Puncture"] = 0.5
    gunnerArmor.ArmorMultiplier["Blast"] = -0.25
    gunnerArmor.ArmorMultiplier["Slash"] = -0.25

    gunnerHealth = Health()
    gunnerHealth.HealthMultiplier["Gas"] = -0.5
    gunnerHealth.HealthMultiplier["Impact"] = -0.25
    gunnerHealth.HealthMultiplier["Heat"] = 0.25
    gunnerHealth.HealthMultiplier["Slash"] = 0.25
    gunnerHealth.HealthMultiplier["Viral"] = 0.75

    gunner = Enemy(gunnerArmor, gunnerHealth)

    damage = []
    for weapon in weapons:
        damage.append(Damage(weapon, gunner))

    #print("Hek Stats: \n" + HekWeap.ShowStats())
    #print("Strun Stats: \n" + StrunWeap.ShowStats())
    #print("Sarpa Stats: \n" + SarpaWeap.ShowStats())

    #procs = SarpaWeap.CalculateProcs()
    #sarpaDmg.CalculateSlashDamage()

    for entry in damage:
        print(entry.weapon.Name + "Projectile: " + format(entry.CalculateSingleshot(), ",f"))
        print(entry.weapon.Name + "Projectile: " + format(entry.CalculateMultishot(), ",f"))
        if entry.weapon.Name == "Sarpa":
            entry.CalculateSlashDamage()

    for entry in damage:
        print(entry.weapon.Name + " Stats:\n" + entry.weapon.ShowStats())
        pass
