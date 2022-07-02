from DamageTypes import DamageTypes

class Mods:
    def __init__(self):
        self.Multiplier = {}
        for entry in DamageTypes().Multiplier:
            self.Multiplier[entry] = 0
