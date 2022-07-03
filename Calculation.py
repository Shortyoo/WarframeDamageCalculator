from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
from Enemy import Enemy
from DamageTypes import DamageTypes
import configparser

config = configparser.ConfigParser()
config.read("Modconfig.ini")
mods = Mods()

for entry in DamageTypes().Multiplier:
    mods.Multiplier[entry] = float(config["Mods"][entry])

hek = Stats()
hek.Damage["Impact"] = 13.1
hek.Damage["Puncture"] = 56.5
hek.Damage["Slash"] = 17.4
hek.Damage["Multishot"] = 7
hek.Damage["StatusChance"] = 13.33
hek.Damage["CritChance"] = 23
hek.Damage["CritDamage"] = 2.1
hek.Damage["Corrosive"] = 52.2

strun = Stats()
strun.Damage["Impact"] = 19.8
strun.Damage["Puncture"] = 6.6
strun.Damage["Slash"] = 17.6
strun.Damage["Multishot"] = 12
strun.Damage["StatusChance"] = 6.7
strun.Damage["CritChance"] = 24
strun.Damage["CritDamage"] = 2.2

sarpa = Stats()
sarpa.Damage["Impact"] = 3.5
sarpa.Damage["Puncture"] = 10.5
sarpa.Damage["Slash"] = 21
sarpa.Damage["Multishot"] = 5
sarpa.Damage["StatusChance"] = 28
sarpa.Damage["CritChance"] = 14
sarpa.Damage["CritDamage"] = 2


# Blood Rush
# Primed Pressure Point
# Organ Shatter
# Condition Overload
# 90 Tox
# 90 Cold

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

HekWeap = Weapon(hek, mods)
StrunWeap = Weapon(strun, mods)
SarpaWeap = Weapon(sarpa, sarpaMods)

gunner = Enemy(gunnerArmor, gunnerHealth)

hekDmg = Damage(HekWeap, gunner)
strunDmg = Damage(StrunWeap, gunner)
sarpaDmg = Damage(SarpaWeap, gunner)

#print("Hek Stats: \n" + HekWeap.ShowStats())
#print("Strun Stats: \n" + StrunWeap.ShowStats())
#print("Sarpa Stats: \n" + SarpaWeap.ShowStats())

procs = SarpaWeap.CalculateProcs()
sarpaDmg.CalculateSlashDamage()

print("Hek Projectile: "+format(hekDmg.CalculateSingleshot(), ",f"))
print("Hek Multishot: " +format(hekDmg.CalculateMultishot(), ",f"))
print("Strun Projectile: "+format(strunDmg.CalculateSingleshot(), ",f"))
print("Strun Multishot: "+format(strunDmg.CalculateMultishot(), ",f"))
print("Sarpa Projectile: "+format(sarpaDmg.CalculateSingleshot(), ",f"))
print("Sarpa Multishot: "+format(sarpaDmg.CalculateMultishot(), ",f"))
