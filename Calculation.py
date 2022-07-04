from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
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

    gunnerStatus = Status()
    gunnerStatus.Status["Viral"] = 0
    gunnerStatus.Status["Corrosive"] = 0
    gunnerStatus.Status["Heat"] = 0
    gunnerStatus.Status["CorrosiveProjection"] = 0

    gunner = Enemy(gunnerHealth, gunnerArmor, gunnerStatus, 88639.62, 8508.85)

    damage = []
    for weapon in weapons:
        damage.append(Damage(weapon, gunner))

    #print("Hek Stats: \n" + HekWeap.ShowStats())
    #print("Strun Stats: \n" + StrunWeap.ShowStats())
    #print("Sarpa Stats: \n" + SarpaWeap.ShowStats())

    #procs = SarpaWeap.CalculateProcs()
    #sarpaDmg.CalculateSlashDamage()

    for entry in damage:
        print(entry.weapon.Name + " with Build: " + entry.weapon.ModName + " Projectile: " + format(entry.CalculateSingleshot(), ",f"))
        print(entry.weapon.Name + " with Build: " + entry.weapon.ModName + " Projectile: " + format(entry.CalculateMultishot(), ",f"))
        firerate = entry.weapon.stats.Damage["FireRate"]
        magsize = entry.weapon.stats.Damage["MagSize"]
        DPS = magsize / firerate
        # If DPS < 1, means that we cant even fire for 1 second.
        # DPS > 1 means we could fire for more than 1 sec, but we want the exact value for 1 sec
        if DPS > 1:
            DPS = entry.weapon.stats.Damage["FireRate"]

        print(entry.weapon.Name + " with Build: " + entry.weapon.ModName + " DPS: " + format(entry.CalculateMultishot() * DPS, ",f"))
        if args.slash:
            tickDamage = float(entry.CalculateSlashDamage())
            print(entry.weapon.Name + "Slash Damage per Tick: " + str(tickDamage))
            print("Damage after 6 Seconds with Slash: " + str(tickDamage * 6))
            print("Total Damage: ")

    if args.showStats:
        for entry in damage:
            print(entry.weapon.Name + " Stats:\n" + entry.weapon.ShowStats(args.showProcs))
