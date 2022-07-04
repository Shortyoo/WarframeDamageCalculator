from DamageTypes import DamageTypes

class Shield:
    def __init__(self):
        self.ShieldMultiplier = {}
        for entry in DamageTypes().Damage:
            self.ShieldMultiplier[entry] = 0
