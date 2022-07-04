from Armor import Armor
from Health import Health
from Status import Status

class Enemy:
    def __init__(self, health, armor, shield, HP, Armor, Shield, status, name):
        self.armor = armor
        self.health = health
        self.status = status
        self.shield = shield
        self.Armor = float(Armor)
        self.HP = float(HP)
        self.Shield = float(Shield)
        self.Name = name
        self.remainingHP = float(HP)
        self.remainingShield = float(Shield)

        #print("Remaining Shield: " + str(self.remainingShield))
        #print("Armor: " + str(self.Armor))
        #print("Remaining HP: " + str(self.remainingHP))
