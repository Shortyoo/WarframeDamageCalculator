from DamageTypes import DamageTypes
import configparser

class Status:
    def __init__(self, status):
        self.Status = {}
        for entry in status.keys():
            self.Status[entry] = status[entry]
        self.DamageTypesInstance = DamageTypes()

    def loadStatus(name: str):

        status = {}

        statusParser = configparser.ConfigParser()
        statusParser.read("ActiveProcs/"+name+".ini")
        DamageTypesInstance = DamageTypes()

        for entry in DamageTypesInstance.Damage:
            status[entry] = int(statusParser["StatusProcs"][entry])

        status["CorrosiveProjection"] = int(statusParser["StatusProcs"]["CorrosiveProjection"])

        return Status(status)

    def GetStatusCount(self):
        count = 0
        for entry in self.DamageTypesInstance.Damage:
            if self.Status[entry] > 0:
                count += 1
        return count
