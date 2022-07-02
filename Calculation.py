from Weapon import Weapon
from Armor import Armor
from Stats import Stats
from Mods import Mods
from Health import Health
from Damage import Damage
from Enemy import Enemy

mods = Mods()
mods.Multiplier["BaseDamage"] = 1.65 # Point Blank
#mods.Multiplier["Corrosive"] = 1.8 # Contagious Spread + Charged Shell
mods.Multiplier["Toxin"] = 0.9
#mods.Multiplier["Electricity"] = 0.9
#mods.Multiplier["CritChance"] = 2 # Critical Deceleration + Zephyr passive
#mods.Multiplier["CritDamage"] = 1.1 # Primed Ravage
#mods.Multiplier["Multishot"] = 2.3 # Full stacked Galvanized Hell

hek = Stats()
hek.Damage["Impact"] = 13.1
hek.Damage["Puncture"] = 56.5
hek.Damage["Slash"] = 17.4
hek.Damage["Multishot"] = 7
hek.Damage["StatusChance"] = 13.33
hek.Damage["CritChance"] = 23
hek.Damage["CritDamage"] = 2.1
hek.Damage["Toxin"] = 52.2

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
# Enduring Affiction
# Organ Shatter
# Primed Pressure Point
# Virulent Scourge 60/60 toxin
# Vicious Frost 60/60 cold

# Check for Condition Overload!
sarpaMods = Mods()
sarpaMods.Multiplier["BaseDamage"] = 2.65 # Primed Pressure Point
sarpaMods.Multiplier["CritChance"] = 5.8 # fully stacked blood rush
sarpaMods.Multiplier["CritDamage"] = 1.9 # Organ Shatter
sarpaMods.Multiplier["StatusChance"] = 3.2 # Enduring Affiction, Viru Scourge
sarpaMods.Multiplier["Viral"] = 1.2
sarpaMods.Multiplier["Cold"] = 0.6
sarpaMods.Multiplier["Toxin"] = 0.6

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
#StrunWeap = Weapon(strun, mods)

gunner = Enemy(gunnerArmor, gunnerHealth)

hekDmg = Damage(HekWeap, gunner)
#strunDmg = Damage(StrunWeap, gunner)

print("Hek Stats: \n" + HekWeap.ShowStats())
#print("Strun Stats: \n" + StrunWeap.ShowStats())

print("Hek Projectile: "+format(hekDmg.CalculateSingleshot(), ",f"))
print("Hek Multishot: " +format(hekDmg.CalculateMultishot(), ",f"))
#print("Strun Projectile: "+format(strunDmg.CalculateSingleshot(), ",f"))
#print("Strun Multishot: "+format(strunDmg.CalculateMultishot(), ",f"))
