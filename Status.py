from DamageTypes import DamageTypes
import configparser

class Status:
    def __init__(self, status):
        self.Status = status

    def loadStatus(name: str):

        status = {}

        statusParser = configparser.ConfigParser()
        statusParser.read("ActiveProcs/"+name+".ini")

        for entry in DamageTypes().Damage:
            status[entry] = int(statusParser["StatusProcs"][entry])

        status["CorrosiveProjection"] = int(statusParser["StatusProcs"]["CorrosiveProjection"])

        return Status(status)

    def GetStatusCount(self):
        count = 0
        for entry in DamageTypes().Damage:
            if self.Status[entry] > 0:
                count = count + 1
        return count
