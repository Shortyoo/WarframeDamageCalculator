from DamageTypes import DamageTypes

class Health:
    def __init__(self):
        self.HealthMultiplier = {}
        for entry in DamageTypes().Damage:
            self.HealthMultiplier[entry] = 0
