class DamageTypes:
    def __init__(self):
        self.Damage = ["Impact", "Puncture", "Slash", "Cold", "Electricity"
        , "Heat", "Toxin", "Blast", "Corrosive", "Gas", "Magnetic", "Radiation"
        , "Viral"]

        self.Multiplier = []

        for entry in self.Damage:
            self.Multiplier.append(entry)

        self.Multiplier.append("BaseDamage")
        self.Multiplier.append("CritChance")
        self.Multiplier.append("CritDamage")
        self.Multiplier.append("StatusChance")
        self.Multiplier.append("Multishot")
        self.Multiplier.append("FactionDamage")
