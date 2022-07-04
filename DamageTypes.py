class DamageTypes:
    def __init__(self):

        self.BaseElementals = ["Cold", "Electricity", "Heat", "Toxin"]
        self.FusedElementals = ["Blast", "Corrosive", "Gas", "Magnetic", "Radiation"
        , "Viral"]
        self.Physical = ["Impact", "Puncture", "Slash"]
        self.Additionals = ["BaseDamage", "CritChance", "CritDamage"
        , "StatusChance", "Multishot", "FactionDamage", "FireRate", "MagSize"]
        self.SpecialMods = ["HunterMunition"]

        self.Elementals = [] # BaseElementals + FusedElementals
        self.Damage = [] # Physical + Elementals
        self.Multiplier = [] # Damage + Additionals

        for entry in self.BaseElementals:
            self.Elementals.append(entry)

        for entry in self.FusedElementals:
            self.Elementals.append(entry)

        for entry in self.Physical:
            self.Damage.append(entry)

        for entry in self.Elementals:
            self.Damage.append(entry)

        for entry in self.Damage:
            self.Multiplier.append(entry)

        for entry in self.Additionals:
            self.Multiplier.append(entry)
