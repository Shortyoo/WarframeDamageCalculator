from DamageTypes import DamageTypes
import configparser

class Mods:
    def __init__(self, name: str):
        self.Name = name
        self.Multiplier = {}
        self.DamageTypesInstance = DamageTypes()
        for entry in DamageTypesInstance.Multiplier:
            self.Multiplier[entry] = 0

        for entry in DamageTypesInstance.SpecialMods:
            self.Multiplier[entry] = 0

    def loadMod(name: str):
        modParser = configparser.ConfigParser()
        modParser.read("Mods/" + name + ".ini")
        mods = Mods(name)
        for entry in DamageTypesInstance.Multiplier:
            mods.Multiplier[entry] = float(modParser["Mods"][entry])
            #print(entry+": " + str(mods.Multiplier[entry]))

        for entry in DamageTypesInstance.SpecialMods:
            if entry in modParser["Mods"]:
                mods.Multiplier[entry] = float(modParser["Mods"][entry])

        if DamageTypesInstance.DamagePerStack in modParser["Mods"]:
            mods.Multiplier[DamageTypesInstance.DamagePerStack] = float(modParser["Mods"][DamageTypesInstance.DamagePerStack])

        return mods
