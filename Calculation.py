from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
from Enemy import Enemy
from DamageTypes import DamageTypes
import configparser
import sys

def loadWeapon(name: str):
    weaponParser = configparser.ConfigParser()
    weaponParser.read("Weapons/"+name+".ini")
    weaponStats = Stats(name)
    for entry in DamageTypes().Multiplier:
        if entry == "BaseDamage" or entry == "FactionDamage":
            continue
        weaponStats.Damage[entry] = float(weaponParser["Weapon"][entry])
    return weaponStats

if len(sys.argv) == 1:
    print("Usage: python Calculation.py \"WeaponName_1\" \"WeaponName_n\"")

weaponStats = []

for name in sys.argv[1::]:
    weaponStats.append(loadWeapon(str(name)))

modParser = configparser.ConfigParser()
modParser.read("Mods/Modconfig_1.ini")
mods = Mods()

for entry in DamageTypes().Multiplier:
    mods.Multiplier[entry] = float(modParser["Mods"][entry])

weapons = []
for stat in weaponStats:
    weapons.append(Weapon(stat, mods))


sarpaMods = Mods()
sarpaMods.Multiplier["BaseDamage"] = 4.85 # 4x Condition Overload
sarpaMods.Multiplier["CritChance"] = 4.8 # fully stacked blood rush
sarpaMods.Multiplier["CritDamage"] = 0.9 # Organ Shatter
sarpaMods.Multiplier["Viral"] = 1.8 # 90 Tox 90 Cold

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
