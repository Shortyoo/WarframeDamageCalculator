from Weapon import Weapon
from Stats import Stats
from Mods import Mods
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

weaponStatList = []
modStatList = []
enemyList = []

calculationParser = configparser.ConfigParser()
calculationParser.read("Calculation.ini")
for entry in calculationParser["Weapons"]:
    weaponStatList.append(Stats.loadWeapon(str(calculationParser["Weapons"][entry])))

for entry in calculationParser["Mods"]:
    modStatList.append(Mods.loadMod(str(calculationParser["Mods"][entry])))

for entry in calculationParser["Enemy"]:
    enemyList.append(Enemy.loadEnemy(str(calculationParser["Enemy"][entry])))

if len(weaponStatList) != len(modStatList) or len(weaponStatList) != len(enemyList) or len(modStatList) != len(enemyList):
    print("Unmatching list-lengths!!")

else:
    weapons = []

    for i in range(0, len(weaponStatList)):
        weapons.append(Weapon(weaponStatList[i], modStatList[i]))

    damage = []

    for i in range(0, len(weapons)):
        damage.append(Damage(weapons[i], enemyList[i]))

    for entry in damage:
        #print("Quantum: " + str(entry.weapon.Quantum))
        #entry.ShootEnemy()
        dmg = entry.CalculateRawDamage()
        print(entry.BuildString() + " Damage against Shield: " + format(dmg[0], ",f"))
        print(entry.BuildString() + " Damage against Health: " + format(dmg[1], ",f"))
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
