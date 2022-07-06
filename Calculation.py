from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
from Shield import Shield
from Enemy import Enemy
from Status import Status
from DamageTypes import DamageTypes
import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sS", "--showStats", help="Shows the stat of each weapon after calculation", action="store_true")
parser.add_argument("-s", "--slash", help ="Calculates the damage of all slash procs", action="store_true")
parser.add_argument("-sP", "--showProcs", help ="Calculates the probability to apply a proc on the opponent", action="store_true")
args = parser.parse_args()

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
    mods = Mods(name)
    for entry in DamageTypes().Multiplier:
        mods.Multiplier[entry] = float(modParser["Mods"][entry])
    return mods

def loadEnemy(name: str):
    enemyParser = configparser.ConfigParser()
    enemyParser.read("Enemies/" + name + ".ini")

    hp = int(enemyParser["Base"]["HP"])
    armor = int(enemyParser["Base"]["Armor"])
    shield = int(enemyParser["Base"]["Shield"])
    baseLevel = int(enemyParser["Base"]["BaseLevel"])
    level = int(enemyParser["Base"]["Level"])
    name = str(enemyParser["Base"]["Name"])

    if level - baseLevel < 70:
        armor = round(armor * (1 + 0.0005 * (level - baseLevel)**1.75), 2)
        hp = round(hp * (1 + 0.015 * (level - baseLevel)**2), 2)
        shield = round(shield * (1 + 0.02*(level - baseLevel)**1.75), 2)
    else:
        armor = round(armor * (1 + 0.4 * (level - baseLevel)**0.75), 2)
        hp = round(hp * (1 + (24*(5**0.5)/5) * (level - baseLevel) ** 0.5), 2)
        shield = round(shield * (1 + 1.6*(level - baseLevel)**0.75), 2)

    if int(enemyParser["Base"]["SteelPath"]) == 1:
        # at first, add the armor value that it gains from + 100 levels
        # https://warframe.fandom.com/wiki/The_Steel_Path

        hp = hp * 2.5
        armor = armor * 2.5
        shield = shield * 2.5

    gunnerArmor = Armor()
    for entry in DamageTypes().Damage:
        gunnerArmor.ArmorMultiplier[entry] = float(enemyParser["Armor"][entry])

    gunnerHealth = Health()
    for entry in DamageTypes().Damage:
        gunnerHealth.HealthMultiplier[entry] = float(enemyParser["Health"][entry])

    gunnerShield = Shield()
    for entry in DamageTypes().Damage:
        gunnerShield.ShieldMultiplier[entry] = float(enemyParser["Shield"][entry])

    gunnerStatus = Status()
    for entry in DamageTypes().Damage:
        gunnerStatus.Status[entry] = float(enemyParser["ActiveProcs"][entry])

    gunnerStatus.Status["CorrosiveProjection"] = enemyParser["ActiveProcs"]["CorrosiveProjection"]

    return Enemy(gunnerHealth, gunnerArmor, gunnerShield, hp, armor, shield, gunnerStatus, name)


weaponStatList = []
modStatList = []
enemyList = []

calculationParser = configparser.ConfigParser()
calculationParser.read("Calculation.ini")
for entry in calculationParser["Weapons"]:
    weaponStatList.append(loadWeapon(str(calculationParser["Weapons"][entry])))

for entry in calculationParser["Mods"]:
    modStatList.append(loadMod(str(calculationParser["Mods"][entry])))

for entry in calculationParser["Enemy"]:
    enemyList.append(loadEnemy(str(calculationParser["Enemy"][entry])))

if len(weaponStatList) != len(modStatList) or len(weaponStatList) != len(enemyList) or len(modStatList) != len(enemyList):
    print("Unmatching list-lengths!!")

else:
    weapons = []

    for i in range(0, len(weaponStatList)):
        weapons.append(Weapon(weaponStatList[i], modStatList[i]))

    damage = []

    for i in range(0, len(weapons)):
        damage.append(Damage(weapons[i], enemyList[i]))

    #print("Hek Stats: \n" + HekWeap.ShowStats())
    #print("Strun Stats: \n" + StrunWeap.ShowStats())
    #print("Sarpa Stats: \n" + SarpaWeap.ShowStats())

    #procs = SarpaWeap.CalculateProcs()
    #sarpaDmg.CalculateSlashDamage()

    for entry in damage:
        print("Quanta: " + str(entry.weapon.Quantum()))
        #entry.ShootEnemy()
        damage = entry.CalculateRawDamage()
        print(entry.BuildString() + " Damage against Shield: " + format(damage[0], ",f"))
        print(entry.BuildString() + " Damage against Health: " + format(damage[1], ",f"))
        firerate = entry.weapon.stats.Damage["FireRate"]
        magsize = entry.weapon.stats.Damage["MagSize"]
        DPS = magsize / firerate
        # If DPS < 1, means that we cant even fire for 1 second.
        # DPS > 1 means we could fire for more than 1 sec, but we want the exact value for 1 sec
        if DPS > 1:
            DPS = entry.weapon.stats.Damage["FireRate"]

        print(entry.BuildString() + " DPS: " + format(entry.CalculateRawDamageMultiShot() * DPS, ",f"))
        if args.slash:
            tickDamage = float(entry.CalculateSlashDamage())
            print(entry.weapon.Name + "Slash Damage per Tick: " + str(tickDamage))
            print("Damage after 6 Seconds with Slash: " + str(tickDamage * 6))
            print("Total Damage: ")

    if args.showStats:
        for entry in damage:
            print(entry.weapon.Name + " Stats:\n" + entry.weapon.ShowStats(args.showProcs))
