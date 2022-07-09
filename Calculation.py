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

if len(calculationParser["Enemy"]) != len(calculationParser["EnemyLevel"]) or len(calculationParser["EnemyLevel"]) != len(calculationParser["ActiveProcs"]):
    print("Unequal lengths of lists \"Enemy\", \"EnemyLevel\", \"ActiveProcs\"")
    exit(-1)

for i in range(len(calculationParser.items("Enemy"))):
    enemyLevel = int(calculationParser.items("EnemyLevel")[i][1])
    activeProcs = Status.loadStatus(str(calculationParser.items("ActiveProcs")[i][1]))
    enemyList.append(Enemy.loadEnemy(str(calculationParser.items("Enemy")[i][1]), enemyLevel, activeProcs))

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
        entry.ShootEnemy()
        entry.PrintRawDamage()

        if args.slash:
            tickDamage = float(entry.CalculateSlashDamage())
            print(entry.weapon.Name + "Slash Damage per Tick: " + str(tickDamage))
            print("Damage after 6 Seconds with Slash: " + str(tickDamage * 6))
            print("Total Damage: ")

    if args.showStats:
        for entry in damage:
            print(entry.weapon.Name + " Stats:\n" + entry.weapon.ShowStats(args.showProcs))
