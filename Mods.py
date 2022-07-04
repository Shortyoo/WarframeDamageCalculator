from DamageTypes import DamageTypes

class Mods:
    def __init__(self, name: str):
        self.Name = name
        self.Multiplier = {}
        for entry in DamageTypes().Multiplier:
            self.Multiplier[entry] = 0
