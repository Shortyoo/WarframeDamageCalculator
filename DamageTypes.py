class DamageTypes:
    def __init__(self):

        self.BaseElementals = ["Cold", "Electricity", "Heat", "Toxin"]
        self.FusedElementals = ["Blast", "Corrosive", "Gas", "Magnetic", "Radiation"
        , "Viral"]

        self.Elementals = []

        for entry in self.BaseElementals:
            self.Elementals.append(entry)

        for entry in self.FusedElementals:
            self.Elementals.append(entry)

        self.Physical = ["Impact", "Puncture", "Slash"]

        self.Damage = []

        for entry in self.Physical:
            self.Damage.append(entry)

        for entry in self.Elementals:
            self.Damage.append(entry)

        self.Additionals = ["BaseDamage", "CritChance", "CritDamage"
        , "StatusChance", "Multishot", "FactionDamage"]

        self.Multiplier = []

        for entry in self.Damage:
            self.Multiplier.append(entry)

        for entry in self.Additionals:
            self.Multiplier.append(entry)
