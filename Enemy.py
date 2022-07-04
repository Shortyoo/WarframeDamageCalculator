from Armor import Armor
from Health import Health
from Status import Status

class Enemy:
    def __init__(self, health, armor, status, HP, Armor):
        self.armor = armor
        self.health = health
        self.status = status
        self.Armor = Armor
        self.HP = HP
