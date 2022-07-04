from Armor import Armor
from Health import Health
from Status import Status

class Enemy:
    def __init__(self, health, armor, shield, HP, Armor, Shield, status, name):
        self.armor = armor
        self.health = health
        self.status = status
        self.Armor = Armor
        self.HP = HP
        self.Shield = Shield
        self.Name = name
