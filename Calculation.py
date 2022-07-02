from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage

mods = Mods()
mods.Multiplier["BaseDamageMultiplier"] = 2.65 # Point Blank
mods.Multiplier["CorrosiveMultiplier"] = 1.8 # Contagious Spread + Charged Shell
mods.Multiplier["CritChanceMultiplier"] = 3 # Critical Deceleration
mods.Multiplier["CritDamageMultiplier"] = 2.1 # Primed Rabvage
mods.Multiplier["MultishotMultiplier"] = 3.3 # Full stacked Galvanized Hell

hek = Stats()
hek.Damage["Impact"] = 13.1
hek.Damage["Puncture"] = 56.5
hek.Damage["Slash"] = 17.4
hek.Damage["Multishot"] = 7
hek.Damage["StatusChance"] = 13.33
hek.Damage["CritChance"] = 23
hek.Damage["CritDamage"] = 2.1
hek.Damage["Corrosive"] = 0


strun = Stats()
strun.Damage["Impact"] = 19.8
strun.Damage["Puncture"] = 6.6
strun.Damage["Slash"] = 17.6
strun.Damage["Multishot"] = 12
strun.Damage["StatusChance"] = 6.7
strun.Damage["CritChance"] = 24
strun.Damage["CritDamage"] = 2.2

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

hekDmg = Damage(HekWeap, gunnerArmor, gunnerHealth)
strunDmg = Damage(StrunWeap, gunnerArmor, gunnerHealth)

print("Hek Projectile: "+str(hekDmg.CalculateSingleshot()))
print("Hek Multishot: " +str(hekDmg.CalculateMultishot()))
print("Strun Projectile: "+str(strunDmg.CalculateSingleshot()))
print("Strun Multishot: "+str(strunDmg.CalculateMultishot()))
