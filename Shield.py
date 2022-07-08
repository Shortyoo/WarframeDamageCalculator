from DamageTypes import DamageTypes

class Shield:
    def __init__(self):
        self.ShieldMultiplier = {}
        self.DamageTypesInstance = DamageTypes()
        for entry in DamageTypesInstance.Damage:
            self.ShieldMultiplier[entry] = 0
