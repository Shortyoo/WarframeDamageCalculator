class DamageResistances:
    def __init__(self):
        self.Resistance = {}

        self.Resistance["Impact"]={}
        self.Resistance["Impact"]["Flesh"]=-0.25
        self.Resistance["Impact"]["Cloned Flesh"]=-0.25
        self.Resistance["Impact"]["Fossilized"]=0.00
        self.Resistance["Impact"]["Infested"]=0.00
        self.Resistance["Impact"]["Infested Flesh"]=0.00
        self.Resistance["Impact"]["Infested Sinew"]=0.00
        self.Resistance["Impact"]["Machinery"]=0.25
        self.Resistance["Impact"]["Robotic"]=0.00
        self.Resistance["Impact"]["Object"]=0.00
        self.Resistance["Impact"]["Shield"]=0.50
        self.Resistance["Impact"]["Proto Shield"]=0.15
        self.Resistance["Impact"]["Ferrite Armor"]=0.00
        self.Resistance["Impact"]["Alloy Armor"]=0.00

        self.Resistance["Puncture"]={}
        self.Resistance["Puncture"]["Flesh"]=0.00
        self.Resistance["Puncture"]["Cloned Flesh"]=0.00
        self.Resistance["Puncture"]["Fossilized"]=0.00
        self.Resistance["Puncture"]["Infested"]=0.00
        self.Resistance["Puncture"]["Infested Flesh"]=0.00
        self.Resistance["Puncture"]["Infested Sinew"]=0.25
        self.Resistance["Puncture"]["Machinery"]=0.00
        self.Resistance["Puncture"]["Robotic"]=0.25
        self.Resistance["Puncture"]["Object"]=0.00
        self.Resistance["Puncture"]["Shield"]=-0.20
        self.Resistance["Puncture"]["Proto Shield"]=-0.50
        self.Resistance["Puncture"]["Ferrite Armor"]=0.50
        self.Resistance["Puncture"]["Alloy Armor"]=0.15

        self.Resistance["Slash"]={}
        self.Resistance["Slash"]["Flesh"]=0.25
        self.Resistance["Slash"]["Cloned Flesh"]=0.25
        self.Resistance["Slash"]["Fossilized"]=0.15
        self.Resistance["Slash"]["Infested"]=0.25
        self.Resistance["Slash"]["Infested Flesh"]=0.50
        self.Resistance["Slash"]["Infested Sinew"]=0.00
        self.Resistance["Slash"]["Machinery"]=0.00
        self.Resistance["Slash"]["Robotic"]=-0.25
        self.Resistance["Slash"]["Object"]=0.00
        self.Resistance["Slash"]["Shield"]=0.00
        self.Resistance["Slash"]["Proto Shield"]=0.00
        self.Resistance["Slash"]["Ferrite Armor"]=-0.15
        self.Resistance["Slash"]["Alloy Armor"]=-0.50

        self.Resistance["Cold"]={}
        self.Resistance["Cold"]["Flesh"]=0.00
        self.Resistance["Cold"]["Cloned Flesh"]=0.00
        self.Resistance["Cold"]["Fossilized"]=-0.25
        self.Resistance["Cold"]["Infested"]=0.00
        self.Resistance["Cold"]["Infested Flesh"]=-0.50
        self.Resistance["Cold"]["Infested Sinew"]=0.25
        self.Resistance["Cold"]["Machinery"]=0.00
        self.Resistance["Cold"]["Robotic"]=0.00
        self.Resistance["Cold"]["Object"]=0.00
        self.Resistance["Cold"]["Shield"]=0.50
        self.Resistance["Cold"]["Proto Shield"]=0.00
        self.Resistance["Cold"]["Ferrite Armor"]=0.00
        self.Resistance["Cold"]["Alloy Armor"]=0.25

        self.Resistance["Electricity"]={}
        self.Resistance["Electricity"]["Flesh"]=0.00
        self.Resistance["Electricity"]["Cloned Flesh"]=0.00
        self.Resistance["Electricity"]["Fossilized"]=0.00
        self.Resistance["Electricity"]["Infested"]=0.00
        self.Resistance["Electricity"]["Infested Flesh"]=0.00
        self.Resistance["Electricity"]["Infested Sinew"]=0.00
        self.Resistance["Electricity"]["Machinery"]=0.50
        self.Resistance["Electricity"]["Robotic"]=0.50
        self.Resistance["Electricity"]["Object"]=0.00
        self.Resistance["Electricity"]["Shield"]=0.00
        self.Resistance["Electricity"]["Proto Shield"]=0.00
        self.Resistance["Electricity"]["Ferrite Armor"]=0.00
        self.Resistance["Electricity"]["Alloy Armor"]=-0.50

        self.Resistance["Heat"]={}
        self.Resistance["Heat"]["Flesh"]=0.00
        self.Resistance["Heat"]["Cloned Flesh"]=0.25
        self.Resistance["Heat"]["Fossilized"]=0.00
        self.Resistance["Heat"]["Infested"]=0.25
        self.Resistance["Heat"]["Infested Flesh"]=0.50
        self.Resistance["Heat"]["Infested Sinew"]=0.00
        self.Resistance["Heat"]["Machinery"]=0.00
        self.Resistance["Heat"]["Robotic"]=0.00
        self.Resistance["Heat"]["Object"]=0.00
        self.Resistance["Heat"]["Shield"]=0.00
        self.Resistance["Heat"]["Proto Shield"]=-0.50
        self.Resistance["Heat"]["Ferrite Armor"]=0.00
        self.Resistance["Heat"]["Alloy Armor"]=0.00

        self.Resistance["Toxin"]={}
        self.Resistance["Toxin"]["Flesh"]=0.50
        self.Resistance["Toxin"]["Cloned Flesh"]=0.00
        self.Resistance["Toxin"]["Fossilized"]=-0.50
        self.Resistance["Toxin"]["Infested"]=0.00
        self.Resistance["Toxin"]["Infested Flesh"]=0.00
        self.Resistance["Toxin"]["Infested Sinew"]=0.00
        self.Resistance["Toxin"]["Machinery"]=-0.25
        self.Resistance["Toxin"]["Robotic"]=-0.25
        self.Resistance["Toxin"]["Object"]=0.00
        self.Resistance["Toxin"]["Shield"]=-1.00 #BYPASS
        self.Resistance["Toxin"]["Proto Shield"]=-1.00 #BYPASS
        self.Resistance["Toxin"]["Ferrite Armor"]=0.00
        self.Resistance["Toxin"]["Alloy Armor"]=0.00

        self.Resistance["Blast"]={}
        self.Resistance["Blast"]["Flesh"]=0.00
        self.Resistance["Blast"]["Cloned Flesh"]=0.00
        self.Resistance["Blast"]["Fossilized"]=0.50
        self.Resistance["Blast"]["Infested"]=0.00
        self.Resistance["Blast"]["Infested Flesh"]=0.00
        self.Resistance["Blast"]["Infested Sinew"]=-0.50
        self.Resistance["Blast"]["Machinery"]=0.75
        self.Resistance["Blast"]["Robotic"]=0.00
        self.Resistance["Blast"]["Object"]=0.00
        self.Resistance["Blast"]["Shield"]=0.00
        self.Resistance["Blast"]["Proto Shield"]=0.00
        self.Resistance["Blast"]["Ferrite Armor"]=-0.25
        self.Resistance["Blast"]["Alloy Armor"]=0.00

        self.Resistance["Corrosive"]={}
        self.Resistance["Corrosive"]["Flesh"]=0.00
        self.Resistance["Corrosive"]["Cloned Flesh"]=0.00
        self.Resistance["Corrosive"]["Fossilized"]=0.75
        self.Resistance["Corrosive"]["Infested"]=0.00
        self.Resistance["Corrosive"]["Infested Flesh"]=0.00
        self.Resistance["Corrosive"]["Infested Sinew"]=0.00
        self.Resistance["Corrosive"]["Machinery"]=0.00
        self.Resistance["Corrosive"]["Robotic"]=0.00
        self.Resistance["Corrosive"]["Object"]=0.00
        self.Resistance["Corrosive"]["Shield"]=0.00
        self.Resistance["Corrosive"]["Proto Shield"]=-0.50
        self.Resistance["Corrosive"]["Ferrite Armor"]=0.75
        self.Resistance["Corrosive"]["Alloy Armor"]=0.00

        self.Resistance["Gas"]={}
        self.Resistance["Gas"]["Flesh"]=-0.25
        self.Resistance["Gas"]["Cloned Flesh"]=-0.50
        self.Resistance["Gas"]["Fossilized"]=0.00
        self.Resistance["Gas"]["Infested"]=0.75
        self.Resistance["Gas"]["Infested Flesh"]=0.50
        self.Resistance["Gas"]["Infested Sinew"]=0.00
        self.Resistance["Gas"]["Machinery"]=0.00
        self.Resistance["Gas"]["Robotic"]=0.00
        self.Resistance["Gas"]["Object"]=0.00
        self.Resistance["Gas"]["Shield"]=0.00
        self.Resistance["Gas"]["Proto Shield"]=0.00
        self.Resistance["Gas"]["Ferrite Armor"]=0.00
        self.Resistance["Gas"]["Alloy Armor"]=0.00

        self.Resistance["Magnetic"]={}
        self.Resistance["Magnetic"]["Flesh"]=0.00
        self.Resistance["Magnetic"]["Cloned Flesh"]=0.00
        self.Resistance["Magnetic"]["Fossilized"]=0.00
        self.Resistance["Magnetic"]["Infested"]=0.00
        self.Resistance["Magnetic"]["Infested Flesh"]=0.00
        self.Resistance["Magnetic"]["Infested Sinew"]=0.00
        self.Resistance["Magnetic"]["Machinery"]=0.00
        self.Resistance["Magnetic"]["Robotic"]=0.00
        self.Resistance["Magnetic"]["Object"]=0.00
        self.Resistance["Magnetic"]["Shield"]=0.75
        self.Resistance["Magnetic"]["Proto Shield"]=0.75
        self.Resistance["Magnetic"]["Ferrite Armor"]=0.00
        self.Resistance["Magnetic"]["Alloy Armor"]=-0.50

        self.Resistance["Radiation"]={}
        self.Resistance["Radiation"]["Flesh"]=0.00
        self.Resistance["Radiation"]["Cloned Flesh"]=0.00
        self.Resistance["Radiation"]["Fossilized"]=-0.75
        self.Resistance["Radiation"]["Infested"]=-0.50
        self.Resistance["Radiation"]["Infested Flesh"]=0.00
        self.Resistance["Radiation"]["Infested Sinew"]=0.50
        self.Resistance["Radiation"]["Machinery"]=0.00
        self.Resistance["Radiation"]["Robotic"]=0.25
        self.Resistance["Radiation"]["Object"]=0.00
        self.Resistance["Radiation"]["Shield"]=-0.25
        self.Resistance["Radiation"]["Proto Shield"]=0.00
        self.Resistance["Radiation"]["Ferrite Armor"]=0.00
        self.Resistance["Radiation"]["Alloy Armor"]=0.75

        self.Resistance["Viral"]={}
        self.Resistance["Viral"]["Flesh"]=0.50
        self.Resistance["Viral"]["Cloned Flesh"]=0.75
        self.Resistance["Viral"]["Fossilized"]=0.00
        self.Resistance["Viral"]["Infested"]=-0.50
        self.Resistance["Viral"]["Infested Flesh"]=0.00
        self.Resistance["Viral"]["Infested Sinew"]=0.00
        self.Resistance["Viral"]["Machinery"]=-0.25
        self.Resistance["Viral"]["Robotic"]=0.00
        self.Resistance["Viral"]["Object"]=0.00
        self.Resistance["Viral"]["Shield"]=0.00
        self.Resistance["Viral"]["Proto Shield"]=0.00
        self.Resistance["Viral"]["Ferrite Armor"]=0.00
        self.Resistance["Viral"]["Alloy Armor"]=0.00


    def GetMultiplier(self, damageType: str, defenseType: str):
        if defenseType == "None":
            return 0
        return self.Resistance[damageType][defenseType]
