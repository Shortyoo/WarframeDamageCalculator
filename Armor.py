from DamageTypes import DamageTypes

class Armor:
    def __init__(self):
        self.ArmorMultiplier = {}
        for entry in DamageTypes().Damage:
            self.ArmorMultiplier[entry] = 0
