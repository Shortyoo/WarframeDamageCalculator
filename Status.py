from DamageTypes import DamageTypes

class Status:
    def __init__(self):
        self.Status = {}

        for entry in DamageTypes().Damage:
            self.Status[entry] = 0

        self.Status["CorrosiveProjection"] = 0
