To use this program, you first have to choose a Weapon, Mod, Enemy, Enemylevel and what active-procs the enemy shall have.
If you cant find your weapon/mod/enemy/active-procs you want, feel free to add it using https://warframe.fandom.com/wiki/WARFRAME_Wiki .

Note: For now, you have to manually calculate your boni using mods. 
I.e.: If you equip Primed Point Blank and you want to have the damage of Galvanized Savvy with 2 stacks and 5 procs of the enemy, you have to calculate your "BaseDamage"-value yourself by simply: 1.65 + (STACKS * 0.4) * PROC_COUNT. Using above exmaple, you would get:
1.65 + (2 * 0.4) * 5 = 1.65 + 0.8 * 5 = 1.65 + 4 = 5.65.

Be aware: As of this version, you have to manually define fused elements. So if you want to calculate the damage for "Amprex" and you want to test it's corrosive damage, you have to define the Amprex as if it would deal corrosive damage, rather than electricity.

The Calculation.ini needs to look at least like this:

	[Weapons]
	weap = Pyrana Prime
	[Mods]
	mods = Pyrana Mod
	[Enemy]
	enemy = Corrupted Heavy Gunner
	[EnemyLevel]
	lv = 145
	[ActiveProcs]
	procs = NoActiveProcs

Make sure anything mentioned (Pyrana Prime, Pyrana Mod, ...) exists in the corresponding folder ("Pyrana Prime" in "Weapons/", "Corrupted Heavy Gunner" in "Enemies/" etc.)

You can then open your commandline* and type "python Calculation.py".
The program was developed using Python 3.8.1.

*  (make sure you navigate to the exact folder. If you dont know how, the simplest way would be to go into the folder "WarframeDamageCalculator", click on that path in the explorer and type "cmd". The commandline will show up with the right path).