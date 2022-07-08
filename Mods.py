from DamageTypes import DamageTypes
import configparser

class Mods:
    def __init__(self, name: str):
        self.Name = name
        self.Multiplier = {}
        for entry in DamageTypes().Multiplier:
            self.Multiplier[entry] = 0

        for entry in DamageTypes().SpecialMods:
            self.Multiplier[entry] = 0

    def loadMod(name: str):
        modParser = configparser.ConfigParser()
        modParser.read("Mods/" + name + ".ini")
        mods = Mods(name)
        for entry in DamageTypes().Multiplier:
            mods.Multiplier[entry] = float(modParser["Mods"][entry])
            #print(entry+": " + str(mods.Multiplier[entry]))

        for entry in DamageTypes().SpecialMods:
            if entry in modParser["Mods"]:
                mods.Multiplier[entry] = float(modParser["Mods"][entry])

        return mods
