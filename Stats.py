from DamageTypes import DamageTypes

class Stats:
    def __init__(self, name: str):
        self.Damage = {}
        for entry in DamageTypes().Multiplier:
            self.Damage[entry] = 0

        self.Name = name
