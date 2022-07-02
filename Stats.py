from DamageTypes import DamageTypes

class Stats:
    def __init__(self):
        self.Damage = {}
        for entry in DamageTypes().Multiplier:
            self.Damage[entry] = 0

    def BaseDamage(self):
        sum = 0
        for entry in DamageTypes().Damage:
            sum = sum + self.Damage[entry]
        return sum

    def Quantum(self):
        return self.BaseDamage() / 16
